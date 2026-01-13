import json
import os
import ssl
import time
import hashlib
import socket
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

from .crypto import (
    create_dpop_token,
    decrypt_response_body,
    derive_session_key,
    encrypt_request_body,
    generate_box_keypair,
    generate_nonce,
    generate_signing_keypair,
    generate_timestamp,
    hmac_sha256,
    PINNED_SPKI_PRIMARY,
    PINNED_SPKI_BACKUP,
    sha256_base64url,
    sha256_hex,
    sign_detached,
)


class SPKIPinningError(Exception):
    pass


class SPKIPinningAdapter(HTTPAdapter):
    def __init__(self, primary_pin: str, backup_pin: str = "", *args, **kwargs):
        self.primary_pin = primary_pin
        self.backup_pin = backup_pin
        super().__init__(*args, **kwargs)
    
    def _get_spki_hash(self, sock: ssl.SSLSocket) -> str:
        try:
            cert_der = sock.getpeercert(binary_form=True)
            if not cert_der:
                return ""
            
            from cryptography import x509
            from cryptography.hazmat.primitives import serialization
            import base64
            
            cert = x509.load_der_x509_certificate(cert_der)
            spki_der = cert.public_key().public_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            spki_hash = hashlib.sha256(spki_der).digest()
            return base64.b64encode(spki_hash).decode('ascii')
        except Exception as e:
            return ""
    
    def send(self, request, *args, **kwargs):
        response = super().send(request, *args, **kwargs)
        
        if self.primary_pin:
            try:
                conn = self.get_connection(request.url)
                if hasattr(conn, 'sock') and conn.sock:
                    server_pin = self._get_spki_hash(conn.sock)
                    if server_pin and server_pin != self.primary_pin:
                        if not self.backup_pin or server_pin != self.backup_pin:
                            raise SPKIPinningError(
                                f"Certificate pin mismatch! Expected: {self.primary_pin}, "
                                f"Got: {server_pin}. Possible MITM attack."
                            )
            except SPKIPinningError:
                raise
            except Exception:
                pass
        
        return response


class AuthGuardError(Exception):
    pass


@dataclass
class Result:
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
    device_id: Optional[str] = None
    refresh_token: Optional[str] = None
    access_token: Optional[str] = None
    access_token_expires_at: Optional[int] = None
    dpop_public_key: Optional[bytes] = None
    dpop_secret_key: Optional[bytes] = None
    session_key: Optional[bytes] = None


class AuthGuardClient:
    DEFAULT_HOST = "api.evora.lol"
    DEFAULT_PORT = 443
    
    def __init__(
        self,
        app_id: str,
        hwid: str,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        use_https: bool = True,
        owner_id: Optional[str] = None,
        sdk_secret: Optional[str] = None,
        storage_path: Optional[str] = None,
        enable_spki_pinning: bool = True,
        spki_pin_primary: Optional[str] = None,
        spki_pin_backup: Optional[str] = None,
    ):
        if not hwid:
            raise ValueError("hwid is required")
        
        self.app_id = app_id
        self.host = host
        self.port = port
        self.use_https = use_https
        self.owner_id = owner_id
        self.hwid = hwid
        self.enable_spki_pinning = enable_spki_pinning
        
        self.device = DeviceState()
        
        self._sdk_secret_temp = sdk_secret
        self._has_sdk_auth = bool(sdk_secret)
        
        if sdk_secret:
            self.device.session_key, _ = derive_session_key(
                sdk_secret, app_id, hwid
            )
        
        scheme = "https" if use_https else "http"
        port_str = "" if (use_https and port == 443) or (not use_https and port == 80) else f":{port}"
        self.base_url = f"{scheme}://{host}{port_str}"
        
        self._spki_pin_primary = spki_pin_primary or PINNED_SPKI_PRIMARY
        self._spki_pin_backup = spki_pin_backup or PINNED_SPKI_BACKUP
        
        self.session_id: Optional[str] = None
        
        self.server_box_public_key_b64: Optional[str] = None
        self.server_box_kid: Optional[str] = None
        
        self.box_public_key: Optional[bytes] = None
        self.box_secret_key: Optional[bytes] = None
        
        if storage_path:
            self.storage_path = Path(storage_path)
        else:
            self.storage_path = Path.home() / ".authguard" / app_id
        
        self._load_device_state()
        
        self._session = requests.Session()
        self._session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "AuthGuard-Python/1.0"
        })
        
        if enable_spki_pinning and use_https:
            pinning_adapter = SPKIPinningAdapter(
                primary_pin=self._spki_pin_primary,
                backup_pin=self._spki_pin_backup
            )
            self._session.mount("https://", pinning_adapter)
    
    def _get_state_file(self) -> Path:
        return self.storage_path / "device_state.json"
    
    def _load_device_state(self) -> None:
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
        if not self.box_public_key or not self.box_secret_key:
            self.box_public_key, self.box_secret_key = generate_box_keypair()
    
    def _ensure_dpop_keypair(self) -> None:
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
        use_raw_dpop: bool = False,
    ) -> Result:
        """Make an HTTP request to the API.
        
        Args:
            method: HTTP method
            path: API path (e.g., "/api/v2/init")
            json_body: JSON request body
            encrypt: Whether to encrypt the body
            use_auth: Whether to include access token
            use_dpop: Whether to include DPoP JWT proof (for authenticated requests)
            use_raw_dpop: Whether to include raw Ed25519 signature (for device init)
            
        Returns:
            Result object
        """
        url = f"{self.base_url}{path}"
        headers = {"x-app-id": self.app_id}
        
        body = json_body or {}
        
        body_json_for_hash = json.dumps(body) if (use_raw_dpop or use_dpop) else None
        
        if encrypt and self.server_box_public_key_b64:
            self._ensure_box_keypair()
            body = encrypt_request_body(
                body,
                self.server_box_public_key_b64,
                self.box_public_key,
                self.box_secret_key,
                self.server_box_kid
            )
        
        if use_auth and self.device.access_token:
            import base64
            headers["Authorization"] = f"Bearer {self.device.access_token}"
            
            if use_dpop:
                self._ensure_dpop_keypair()
                
                ts = str(int(time.time() * 1000))
                nonce = generate_nonce()
                body_hash = sha256_hex(body_json_for_hash.encode('utf-8')) if body_json_for_hash else sha256_hex(b'')
                access_token_hash = sha256_hex(self.device.access_token.encode('utf-8'))
                payload = f"{method}:{path}:{ts}:{nonce}:{body_hash}:{access_token_hash}"
                
                signature = sign_detached(payload.encode('utf-8'), self.device.dpop_secret_key)
                sig_b64 = base64.b64encode(signature).decode('ascii')
                
                headers["x-timestamp"] = ts
                headers["x-nonce"] = nonce
                headers["x-dpop"] = sig_b64
        
        if use_raw_dpop and not use_auth:
            import base64
            self._ensure_dpop_keypair()
            
            ts = str(int(time.time() * 1000))
            nonce = generate_nonce()
            body_hash = sha256_hex(body_json_for_hash.encode('utf-8'))
            payload = f"{method}:{path}:{ts}:{nonce}:{body_hash}"
            
            signature = sign_detached(payload.encode('utf-8'), self.device.dpop_secret_key)
            sig_b64 = base64.b64encode(signature).decode('ascii')
            
            headers["x-timestamp"] = ts
            headers["x-nonce"] = nonce
            headers["x-dpop"] = sig_b64
        
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
            
            if response_data.get("v2Encrypted") and self.server_box_public_key_b64:
                try:
                    response_data = decrypt_response_body(
                        response_data,
                        self.box_secret_key,
                        self.server_box_public_key_b64
                    )
                except Exception as e:
                    return Result.failure(f"Decryption failed: {e}")
            
            if response_data.get("success") is False:
                error_msg = response_data.get("message") or response_data.get("error", "")
                if isinstance(error_msg, dict):
                    error_msg = error_msg.get("message", str(error_msg))
                return Result.failure(str(error_msg) or raw_json[:200])
            
            return Result.success(response_data, raw_json)
            
        except requests.Timeout:
            return Result.failure("Request timed out")
        except requests.RequestException as e:
            return Result.failure(f"Request failed: {e}")
    
    def _fetch_server_key(self) -> Result:
        result = self._make_request("POST", "/api/v2/crypto/pubkey")
        if result.ok:
            self.server_box_public_key_b64 = result.data.get("public_key_base64") or result.data.get("public_key")
            self.server_box_kid = result.data.get("kid")
        return result
    
    def init_session(self) -> Result:
        key_result = self._fetch_server_key()
        if not key_result.ok:
            return key_result
        
        self._ensure_box_keypair()
        
        payload = {"hwid": self.hwid}
        
        if self.owner_id and self._sdk_secret_temp:
            payload["owner_id"] = self.owner_id
            payload["sdk_secret"] = self._sdk_secret_temp
        
        result = self._make_request("POST", "/api/v2/init", payload, encrypt=True)
        
        if result.ok:
            self.session_id = result.data.get("sessionid")
        
        if self._sdk_secret_temp:
            from .crypto import secure_zero_memory
            if isinstance(self._sdk_secret_temp, str):
                temp_bytes = bytearray(self._sdk_secret_temp.encode('utf-8'))
                secure_zero_memory(temp_bytes)
            self._sdk_secret_temp = None
        
        return result
    
    def ensure_device(self) -> Result:
        if not self.session_id:
            init_result = self.init_session()
            if not init_result.ok:
                return init_result
        
        if self.device.device_id and self.device.refresh_token:
            return self._refresh_tokens()
        else:
            return self._register_device()
    
    def _register_device(self) -> Result:
        self._ensure_box_keypair()
        self._ensure_dpop_keypair()
        
        import base64
        
        payload = {
            "sessionid": self.session_id,
            "public_key_base64": base64.b64encode(self.device.dpop_public_key).decode('ascii'),
        }
        if self.hwid:
            payload["hwid"] = self.hwid
        
        result = self._make_request("POST", "/api/v2/device/init", payload, encrypt=True, use_raw_dpop=True)
        
        if result.ok:
            self.device.device_id = result.data.get("device_id")
            self.device.refresh_token = result.data.get("refresh_token")
            self.device.access_token = result.data.get("access_token")
            
            expires_in = result.data.get("expires_in", 900)
            self.device.access_token_expires_at = int(time.time()) + expires_in - 60
            
            self._save_device_state()
        
        return result
    
    def _refresh_tokens(self) -> Result:
        self._ensure_box_keypair()
        self._ensure_dpop_keypair()
        
        payload = {
            "refresh_token": self.device.refresh_token,
        }
        
        if self.session_id:
            payload["sessionid"] = self.session_id
        
        result = self._make_request("POST", "/api/v2/device/refresh", payload, encrypt=True, use_raw_dpop=True)
        
        if result.ok:
            self.device.refresh_token = result.data.get("refresh_token", self.device.refresh_token)
            self.device.access_token = result.data.get("access_token")
            
            expires_in = result.data.get("expires_in", 900)
            self.device.access_token_expires_at = int(time.time()) + expires_in - 60
            
            self._save_device_state()
        elif "invalid" in str(result.error).lower() or "expired" in str(result.error).lower():
            self.device = DeviceState()
            self._save_device_state()
            return self._register_device()
        
        return result
    
    def ensure_access_token(self) -> Result:
        if not self.device.access_token:
            return self.ensure_device()
        
        if self.device.access_token_expires_at and time.time() >= self.device.access_token_expires_at:
            return self._refresh_tokens()
        
        return Result.success({"access_token": self.device.access_token})
    
    def login(self, username: str, password: str, hwid: Optional[str] = None) -> Result:
        token_result = self.ensure_access_token()
        if not token_result.ok:
            return token_result
        
        payload = {
            "username": username,
            "password": password,
            "hwid": hwid or self.hwid,
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
