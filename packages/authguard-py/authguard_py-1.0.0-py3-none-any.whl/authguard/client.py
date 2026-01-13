"""
AuthGuard Client - Main SDK entry point.

Implements the AuthGuard v2 API flow:
1. POST /api/v2/init - Bootstrap session
2. POST /api/v2/crypto/pubkey - Get server encryption key
3. POST /api/v2/device/init - Register device, get tokens
4. POST /api/v2/device/refresh - Refresh access token
5. Protected calls with Bearer token + DPoP
"""

import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

import requests

from .crypto import (
    create_dpop_token,
    decrypt_response_body,
    encrypt_request_body,
    generate_box_keypair,
    generate_hwid,
    generate_nonce,
    generate_signing_keypair,
    generate_timestamp,
    sha256_base64url,
)


class AuthGuardError(Exception):
    """Base exception for AuthGuard SDK errors."""
    pass


@dataclass
class Result:
    """Result of an API call."""
    ok: bool
    error: Optional[str] = None
    data: Dict[str, Any] = field(default_factory=dict)
    raw_json: Optional[str] = None
    
    @classmethod
    def success(cls, data: Dict[str, Any], raw_json: str = None) -> "Result":
        return cls(ok=True, data=data, raw_json=raw_json)
    
    @classmethod
    def failure(cls, error: str) -> "Result":
        return cls(ok=False, error=error)


@dataclass
class DeviceState:
    """Persistent device state."""
    device_id: Optional[str] = None
    refresh_token: Optional[str] = None
    access_token: Optional[str] = None
    access_token_expires_at: Optional[int] = None
    dpop_public_key: Optional[bytes] = None
    dpop_secret_key: Optional[bytes] = None


class AuthGuardClient:
    """AuthGuard v2 API client with encrypted communications."""
    
    DEFAULT_HOST = "api.evora.lol"
    DEFAULT_PORT = 443
    
    def __init__(
        self,
        app_id: str,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        use_https: bool = True,
        owner_id: Optional[str] = None,
        sdk_secret: Optional[str] = None,
        hwid: Optional[str] = None,
        storage_path: Optional[str] = None,
    ):
        """Initialize the AuthGuard client.
        
        Args:
            app_id: Application UUID
            host: API host (default: api.evora.lol)
            port: API port (default: 443)
            use_https: Use HTTPS (default: True)
            owner_id: Developer user ID for SDK auth
            sdk_secret: SDK secret for developer auth
            hwid: Hardware ID (auto-generated if None)
            storage_path: Path for device state storage
        """
        self.app_id = app_id
        self.host = host
        self.port = port
        self.use_https = use_https
        self.owner_id = owner_id
        self.sdk_secret = sdk_secret
        self.hwid = hwid or generate_hwid()
        
        # Base URL
        scheme = "https" if use_https else "http"
        port_str = "" if (use_https and port == 443) or (not use_https and port == 80) else f":{port}"
        self.base_url = f"{scheme}://{host}{port_str}"
        
        # Session state
        self.session_id: Optional[str] = None
        
        # Server encryption key
        self.server_box_public_key_b64: Optional[str] = None
        self.server_box_kid: Optional[str] = None
        
        # Client encryption keypair (regenerated per session)
        self.box_public_key: Optional[bytes] = None
        self.box_secret_key: Optional[bytes] = None
        
        # Device state (persistent)
        self.device = DeviceState()
        
        # Storage
        if storage_path:
            self.storage_path = Path(storage_path)
        else:
            # Default to user's home directory
            self.storage_path = Path.home() / ".authguard" / app_id
        
        # Load existing device state
        self._load_device_state()
        
        # HTTP session
        self._session = requests.Session()
        self._session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "AuthGuard-Python/1.0"
        })
    
    def _get_state_file(self) -> Path:
        """Get path to device state file."""
        return self.storage_path / "device_state.json"
    
    def _load_device_state(self) -> None:
        """Load device state from disk."""
        state_file = self._get_state_file()
        if state_file.exists():
            try:
                with open(state_file, 'r') as f:
                    data = json.load(f)
                self.device.device_id = data.get("device_id")
                self.device.refresh_token = data.get("refresh_token")
                self.device.access_token = data.get("access_token")
                self.device.access_token_expires_at = data.get("access_token_expires_at")
                if data.get("dpop_public_key"):
                    self.device.dpop_public_key = bytes.fromhex(data["dpop_public_key"])
                if data.get("dpop_secret_key"):
                    self.device.dpop_secret_key = bytes.fromhex(data["dpop_secret_key"])
            except Exception:
                pass
    
    def _save_device_state(self) -> None:
        """Save device state to disk."""
        self.storage_path.mkdir(parents=True, exist_ok=True)
        state_file = self._get_state_file()
        
        data = {
            "device_id": self.device.device_id,
            "refresh_token": self.device.refresh_token,
            "access_token": self.device.access_token,
            "access_token_expires_at": self.device.access_token_expires_at,
        }
        if self.device.dpop_public_key:
            data["dpop_public_key"] = self.device.dpop_public_key.hex()
        if self.device.dpop_secret_key:
            data["dpop_secret_key"] = self.device.dpop_secret_key.hex()
        
        with open(state_file, 'w') as f:
            json.dump(data, f)
    
    def _ensure_box_keypair(self) -> None:
        """Ensure we have a box keypair for encryption."""
        if not self.box_public_key or not self.box_secret_key:
            self.box_public_key, self.box_secret_key = generate_box_keypair()
    
    def _ensure_dpop_keypair(self) -> None:
        """Ensure we have a DPoP signing keypair."""
        if not self.device.dpop_public_key or not self.device.dpop_secret_key:
            self.device.dpop_public_key, self.device.dpop_secret_key = generate_signing_keypair()
            self._save_device_state()
    
    def _make_request(
        self,
        method: str,
        path: str,
        json_body: Optional[dict] = None,
        encrypt: bool = False,
        use_auth: bool = False,
        use_dpop: bool = False,
    ) -> Result:
        """Make an HTTP request to the API.
        
        Args:
            method: HTTP method
            path: API path (e.g., "/api/v2/init")
            json_body: JSON request body
            encrypt: Whether to encrypt the body
            use_auth: Whether to include access token
            use_dpop: Whether to include DPoP proof
            
        Returns:
            Result object
        """
        url = f"{self.base_url}{path}"
        headers = {"x-app-id": self.app_id}
        
        # Prepare body
        body = json_body or {}
        
        if encrypt and self.server_box_public_key_b64:
            self._ensure_box_keypair()
            body = encrypt_request_body(
                body,
                self.server_box_public_key_b64,
                self.box_public_key,
                self.box_secret_key,
                self.server_box_kid
            )
        
        # Add auth headers
        if use_auth and self.device.access_token:
            headers["Authorization"] = f"Bearer {self.device.access_token}"
            
            # Add timestamp and nonce for PoP
            if use_dpop:
                headers["x-timestamp"] = str(generate_timestamp())
                headers["x-nonce"] = generate_nonce()
                
                # Create DPoP token
                self._ensure_dpop_keypair()
                ath = sha256_base64url(self.device.access_token)
                dpop = create_dpop_token(
                    method,
                    url,
                    self.device.dpop_secret_key,
                    self.device.dpop_public_key,
                    ath
                )
                headers["x-dpop"] = dpop
        
        try:
            response = self._session.request(
                method,
                url,
                json=body,
                headers=headers,
                timeout=30
            )
            
            raw_json = response.text
            
            try:
                response_data = response.json()
            except:
                return Result.failure(f"Invalid JSON response: {raw_json[:200]}")
            
            # Decrypt response if needed
            if response_data.get("v2Encrypted") and self.server_box_public_key_b64:
                try:
                    response_data = decrypt_response_body(
                        response_data,
                        self.box_secret_key,
                        self.server_box_public_key_b64
                    )
                except Exception as e:
                    return Result.failure(f"Decryption failed: {e}")
            
            # Check for API success
            if response_data.get("success") is False:
                error_msg = response_data.get("error", {})
                if isinstance(error_msg, dict):
                    error_msg = error_msg.get("message", str(error_msg))
                return Result.failure(str(error_msg))
            
            return Result.success(response_data, raw_json)
            
        except requests.Timeout:
            return Result.failure("Request timed out")
        except requests.RequestException as e:
            return Result.failure(f"Request failed: {e}")
    
    def _fetch_server_key(self) -> Result:
        """Fetch the server's box public key."""
        result = self._make_request("POST", "/api/v2/crypto/pubkey")
        if result.ok:
            self.server_box_public_key_b64 = result.data.get("public_key")
            self.server_box_kid = result.data.get("kid")
        return result
    
    def init_session(self) -> Result:
        """Initialize app session (bootstrap).
        
        This must be called first to establish a session.
        """
        # First, get the server's encryption key
        key_result = self._fetch_server_key()
        if not key_result.ok:
            return key_result
        
        self._ensure_box_keypair()
        
        # Build init payload
        payload = {"hwid": self.hwid}
        
        # Add SDK auth if configured
        if self.owner_id and self.sdk_secret:
            payload["owner_id"] = self.owner_id
            payload["sdk_secret"] = self.sdk_secret
        
        result = self._make_request("POST", "/api/v2/init", payload, encrypt=True)
        
        if result.ok:
            self.session_id = result.data.get("session_id")
        
        return result
    
    def ensure_device(self) -> Result:
        """Ensure device is registered and has valid tokens.
        
        If device is not registered, registers it.
        If access token is expired, refreshes it.
        """
        if not self.session_id:
            init_result = self.init_session()
            if not init_result.ok:
                return init_result
        
        # Check if we have a device registered
        if self.device.device_id and self.device.refresh_token:
            # Try to refresh
            return self._refresh_tokens()
        else:
            # Register new device
            return self._register_device()
    
    def _register_device(self) -> Result:
        """Register a new device."""
        self._ensure_box_keypair()
        self._ensure_dpop_keypair()
        
        import base64
        
        payload = {
            "session_id": self.session_id,
            "hwid": self.hwid,
            "device_public_key": base64.b64encode(self.device.dpop_public_key).decode('ascii'),
        }
        
        result = self._make_request("POST", "/api/v2/device/init", payload, encrypt=True)
        
        if result.ok:
            self.device.device_id = result.data.get("device_id")
            self.device.refresh_token = result.data.get("refresh_token")
            self.device.access_token = result.data.get("access_token")
            
            # Calculate expiry (access tokens typically last 15 minutes)
            expires_in = result.data.get("expires_in", 900)
            self.device.access_token_expires_at = int(time.time()) + expires_in - 60
            
            self._save_device_state()
        
        return result
    
    def _refresh_tokens(self) -> Result:
        """Refresh access token using refresh token."""
        self._ensure_box_keypair()
        
        payload = {
            "refresh_token": self.device.refresh_token,
        }
        
        result = self._make_request("POST", "/api/v2/device/refresh", payload, encrypt=True)
        
        if result.ok:
            self.device.refresh_token = result.data.get("refresh_token", self.device.refresh_token)
            self.device.access_token = result.data.get("access_token")
            
            expires_in = result.data.get("expires_in", 900)
            self.device.access_token_expires_at = int(time.time()) + expires_in - 60
            
            self._save_device_state()
        elif "invalid" in str(result.error).lower() or "expired" in str(result.error).lower():
            # Refresh token invalid, need to re-register
            self.device = DeviceState()
            self._save_device_state()
            return self._register_device()
        
        return result
    
    def ensure_access_token(self) -> Result:
        """Ensure we have a valid access token."""
        if not self.device.access_token:
            return self.ensure_device()
        
        # Check if token is expired
        if self.device.access_token_expires_at and time.time() >= self.device.access_token_expires_at:
            return self._refresh_tokens()
        
        return Result.success({"access_token": self.device.access_token})
    
    def login(self, username: str, password: str) -> Result:
        """Authenticate with username and password.
        
        Args:
            username: Account username
            password: Account password
            
        Returns:
            Result with user data on success
        """
        token_result = self.ensure_access_token()
        if not token_result.ok:
            return token_result
        
        payload = {
            "username": username,
            "password": password,
        }
        
        return self._make_request(
            "POST", "/api/v2/login", payload,
            encrypt=True, use_auth=True, use_dpop=True
        )
    
    def register(
        self,
        username: str,
        password: str,
        email: Optional[str] = None,
        key: Optional[str] = None
    ) -> Result:
        """Register a new account.
        
        Args:
            username: Desired username
            password: Account password
            email: Optional email address
            key: Optional license key to attach
            
        Returns:
            Result with user data on success
        """
        token_result = self.ensure_access_token()
        if not token_result.ok:
            return token_result
        
        payload = {
            "username": username,
            "password": password,
        }
        if email:
            payload["email"] = email
        if key:
            payload["key"] = key
        
        return self._make_request(
            "POST", "/api/v2/register", payload,
            encrypt=True, use_auth=True, use_dpop=True
        )
    
    def license(self, license_key: str) -> Result:
        """Authenticate with a license key.
        
        Args:
            license_key: The license key
            
        Returns:
            Result with license data on success
        """
        token_result = self.ensure_access_token()
        if not token_result.ok:
            return token_result
        
        payload = {"key": license_key}
        
        return self._make_request(
            "POST", "/api/v2/license", payload,
            encrypt=True, use_auth=True, use_dpop=True
        )
    
    def upgrade(self, license_key: str) -> Result:
        """Upgrade account with a license key.
        
        Args:
            license_key: The upgrade license key
            
        Returns:
            Result with updated subscription data
        """
        token_result = self.ensure_access_token()
        if not token_result.ok:
            return token_result
        
        payload = {"key": license_key}
        
        return self._make_request(
            "POST", "/api/v2/upgrade", payload,
            encrypt=True, use_auth=True, use_dpop=True
        )
    
    def check(self) -> Result:
        """Check if the current session is valid.
        
        Returns:
            Result with session info
        """
        token_result = self.ensure_access_token()
        if not token_result.ok:
            return token_result
        
        return self._make_request(
            "POST", "/api/v2/check", {},
            encrypt=True, use_auth=True, use_dpop=True
        )
    
    def heartbeat(self) -> Result:
        """Send a heartbeat to keep the session alive.
        
        Returns:
            Result with heartbeat response
        """
        token_result = self.ensure_access_token()
        if not token_result.ok:
            return token_result
        
        return self._make_request(
            "POST", "/api/v2/heartbeat", {},
            encrypt=True, use_auth=True, use_dpop=True
        )
    
    def get_var(self, name: str) -> Result:
        """Get an application variable.
        
        Args:
            name: Variable name
            
        Returns:
            Result with variable value
        """
        token_result = self.ensure_access_token()
        if not token_result.ok:
            return token_result
        
        payload = {"name": name}
        
        return self._make_request(
            "POST", "/api/v2/var", payload,
            encrypt=True, use_auth=True, use_dpop=True
        )
    
    def log(self, action: str, data: Optional[dict] = None) -> Result:
        """Log an event to the server.
        
        Args:
            action: Action/event name
            data: Optional additional data
            
        Returns:
            Result confirming log was received
        """
        token_result = self.ensure_access_token()
        if not token_result.ok:
            return token_result
        
        payload = {"action": action}
        if data:
            payload["data"] = data
        
        return self._make_request(
            "POST", "/api/v2/log", payload,
            encrypt=True, use_auth=True, use_dpop=True
        )
    
    def anti_debug_report_early(
        self,
        method: str,
        details: Optional[dict] = None,
        hwid: Optional[str] = None,
        process: Optional[str] = None,
        windows_username: Optional[str] = None,
        screenshot: Optional[str] = None,
    ) -> Result:
        """Report anti-debug detection (pre-login, unauthenticated).
        
        Use this when detection occurs before user login.
        
        Args:
            method: Detection method (e.g., "IsDebuggerPresent", "timing_check")
            details: Additional detection details
            hwid: Hardware ID (defaults to client's hwid)
            process: Process name
            windows_username: Windows username
            screenshot: Base64 encoded screenshot
            
        Returns:
            Result confirming report was received
        """
        if not self.server_box_public_key_b64:
            key_result = self._fetch_server_key()
            if not key_result.ok:
                return key_result
        
        payload = {
            "method": method,
            "hwid": hwid or self.hwid,
        }
        if details:
            payload["details"] = details
        if process:
            payload["process"] = process
        if windows_username:
            payload["windows_username"] = windows_username
        if screenshot:
            payload["screenshot"] = screenshot
        
        return self._make_request(
            "POST", "/api/v2/anti-debug/report-early", payload,
            encrypt=True, use_auth=False, use_dpop=False
        )
    
    def anti_debug_report(
        self,
        method: str,
        details: Optional[dict] = None,
        hwid: Optional[str] = None,
        process: Optional[str] = None,
        windows_username: Optional[str] = None,
        screenshot: Optional[str] = None,
    ) -> Result:
        """Report anti-debug detection (authenticated).
        
        Use this when detection occurs after user login.
        
        Args:
            method: Detection method (e.g., "IsDebuggerPresent", "timing_check")
            details: Additional detection details
            hwid: Hardware ID (defaults to client's hwid)
            process: Process name
            windows_username: Windows username
            screenshot: Base64 encoded screenshot
            
        Returns:
            Result confirming report was received
        """
        token_result = self.ensure_access_token()
        if not token_result.ok:
            return token_result
        
        payload = {
            "method": method,
            "hwid": hwid or self.hwid,
        }
        if details:
            payload["details"] = details
        if process:
            payload["process"] = process
        if windows_username:
            payload["windows_username"] = windows_username
        if screenshot:
            payload["screenshot"] = screenshot
        
        return self._make_request(
            "POST", "/api/v2/anti-debug/report", payload,
            encrypt=True, use_auth=True, use_dpop=True
        )
    
    def call_protected(self, path: str, data: dict) -> Result:
        """Make an authenticated API call to a custom endpoint.
        
        Args:
            path: API path (should start with /api/v2/)
            data: Request body
            
        Returns:
            Result with response data
        """
        token_result = self.ensure_access_token()
        if not token_result.ok:
            return token_result
        
        return self._make_request(
            "POST", path, data,
            encrypt=True, use_auth=True, use_dpop=True
        )
    
    def call_bootstrap(self, path: str, data: dict) -> Result:
        """Make a bootstrap API call (no auth required).
        
        Args:
            path: API path
            data: Request body
            
        Returns:
            Result with response data
        """
        if not self.server_box_public_key_b64:
            key_result = self._fetch_server_key()
            if not key_result.ok:
                return key_result
        
        return self._make_request("POST", path, data, encrypt=True)
