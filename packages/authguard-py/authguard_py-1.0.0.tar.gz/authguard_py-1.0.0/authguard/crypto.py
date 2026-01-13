"""
Cryptographic utilities for AuthGuard SDK.

Uses NaCl (libsodium) for:
- box encryption (Curve25519 + XSalsa20-Poly1305)
- Ed25519 signing for DPoP tokens
"""

import base64
import json
import os
import secrets
import time
import hashlib
from typing import Optional, Tuple

from nacl.public import PrivateKey, PublicKey, Box
from nacl.signing import SigningKey
from nacl.encoding import Base64Encoder


def generate_box_keypair() -> Tuple[bytes, bytes]:
    """Generate a NaCl box keypair (Curve25519).
    
    Returns:
        Tuple of (public_key, secret_key) as bytes
    """
    private_key = PrivateKey.generate()
    public_key = private_key.public_key
    return bytes(public_key), bytes(private_key)


def generate_signing_keypair() -> Tuple[bytes, bytes]:
    """Generate an Ed25519 signing keypair.
    
    Returns:
        Tuple of (public_key, secret_key) as bytes
    """
    signing_key = SigningKey.generate()
    verify_key = signing_key.verify_key
    return bytes(verify_key), bytes(signing_key)


def encrypt_box(
    plaintext: bytes,
    recipient_public_key: bytes,
    sender_secret_key: bytes
) -> Tuple[bytes, bytes]:
    """Encrypt data using NaCl box.
    
    Args:
        plaintext: Data to encrypt
        recipient_public_key: Server's public key
        sender_secret_key: Client's secret key
        
    Returns:
        Tuple of (nonce, ciphertext)
    """
    box = Box(PrivateKey(sender_secret_key), PublicKey(recipient_public_key))
    nonce = secrets.token_bytes(24)  # 24-byte nonce for XSalsa20
    ciphertext = box.encrypt(plaintext, nonce)
    # Box.encrypt returns nonce + ciphertext, we want them separate
    return nonce, ciphertext.ciphertext


def decrypt_box(
    ciphertext: bytes,
    nonce: bytes,
    sender_public_key: bytes,
    recipient_secret_key: bytes
) -> bytes:
    """Decrypt data using NaCl box.
    
    Args:
        ciphertext: Encrypted data
        nonce: 24-byte nonce
        sender_public_key: Server's public key
        recipient_secret_key: Client's secret key
        
    Returns:
        Decrypted plaintext
    """
    box = Box(PrivateKey(recipient_secret_key), PublicKey(sender_public_key))
    return box.decrypt(ciphertext, nonce)


def encrypt_request_body(
    json_body: dict,
    server_public_key_b64: str,
    client_public_key: bytes,
    client_secret_key: bytes,
    kid: Optional[str] = None
) -> dict:
    """Encrypt a JSON request body for the v2 API.
    
    Args:
        json_body: The JSON data to encrypt
        server_public_key_b64: Server's box public key (base64)
        client_public_key: Client's box public key
        client_secret_key: Client's box secret key
        kid: Key ID for the server key
        
    Returns:
        Encrypted payload dict ready for JSON serialization
    """
    server_public_key = base64.b64decode(server_public_key_b64)
    plaintext = json.dumps(json_body).encode('utf-8')
    
    nonce, ciphertext = encrypt_box(plaintext, server_public_key, client_secret_key)
    
    payload = {
        "v2Encrypted": True,
        "ciphertext": base64.b64encode(ciphertext).decode('ascii'),
        "nonce": base64.b64encode(nonce).decode('ascii'),
        "clientPubKey": base64.b64encode(client_public_key).decode('ascii'),
    }
    
    if kid:
        payload["kid"] = kid
        
    return payload


def decrypt_response_body(
    encrypted_response: dict,
    client_secret_key: bytes,
    server_public_key_b64: str
) -> dict:
    """Decrypt an encrypted response from the v2 API.
    
    Args:
        encrypted_response: The encrypted response dict
        client_secret_key: Client's box secret key
        server_public_key_b64: Server's box public key (base64)
        
    Returns:
        Decrypted JSON response
    """
    if not encrypted_response.get("v2Encrypted"):
        return encrypted_response
    
    server_public_key = base64.b64decode(server_public_key_b64)
    ciphertext = base64.b64decode(encrypted_response["ciphertext"])
    nonce = base64.b64decode(encrypted_response["nonce"])
    
    plaintext = decrypt_box(ciphertext, nonce, server_public_key, client_secret_key)
    return json.loads(plaintext.decode('utf-8'))


def generate_nonce() -> str:
    """Generate a random nonce for request signing."""
    return secrets.token_hex(16)


def generate_timestamp() -> int:
    """Generate current Unix timestamp."""
    return int(time.time())


def create_dpop_token(
    method: str,
    uri: str,
    signing_secret_key: bytes,
    signing_public_key: bytes,
    access_token_hash: Optional[str] = None
) -> str:
    """Create a DPoP (Proof-of-Possession) token.
    
    Args:
        method: HTTP method (e.g., "POST")
        uri: Full request URI
        signing_secret_key: Ed25519 signing key
        signing_public_key: Ed25519 verify key
        access_token_hash: Optional SHA-256 hash of access token
        
    Returns:
        DPoP JWT token
    """
    signing_key = SigningKey(signing_secret_key)
    
    # JWT Header
    header = {
        "typ": "dpop+jwt",
        "alg": "EdDSA",
        "jwk": {
            "kty": "OKP",
            "crv": "Ed25519",
            "x": base64.urlsafe_b64encode(signing_public_key).rstrip(b'=').decode('ascii')
        }
    }
    
    # JWT Payload
    payload = {
        "jti": secrets.token_hex(16),
        "htm": method.upper(),
        "htu": uri,
        "iat": int(time.time()),
    }
    
    if access_token_hash:
        payload["ath"] = access_token_hash
    
    # Encode header and payload
    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).rstrip(b'=').decode('ascii')
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b'=').decode('ascii')
    
    # Sign
    message = f"{header_b64}.{payload_b64}".encode('utf-8')
    signature = signing_key.sign(message).signature
    signature_b64 = base64.urlsafe_b64encode(signature).rstrip(b'=').decode('ascii')
    
    return f"{header_b64}.{payload_b64}.{signature_b64}"


def sha256_base64url(data: str) -> str:
    """Compute SHA-256 hash and return as base64url."""
    h = hashlib.sha256(data.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(h).rstrip(b'=').decode('ascii')


def generate_hwid() -> str:
    """Generate a hardware ID.
    
    In a real implementation, this would gather system-specific info.
    For Python SDK, we generate a persistent random ID.
    """
    # Try to get machine-specific ID
    try:
        import uuid
        # Get MAC address-based UUID
        mac = uuid.getnode()
        # Combine with some entropy
        combined = f"{mac}-{os.name}-python"
        return hashlib.sha256(combined.encode()).hexdigest()[:32]
    except:
        # Fallback to random
        return secrets.token_hex(16)
