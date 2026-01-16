import base64
import json
import os
import secrets
import time
import hashlib
import ctypes
from typing import Optional, Tuple

from nacl.public import PrivateKey, PublicKey, Box
from nacl.signing import SigningKey
from nacl.encoding import Base64Encoder

PINNED_SPKI_PRIMARY = "taIhRkC3wgnGShhsUHBzi+8l871vrGvgiHJu+yC4FLU="
PINNED_SPKI_BACKUP = ""


def secure_zero_memory(data: bytearray) -> None:
    if not isinstance(data, bytearray):
        return
    
    try:
        ctypes.memset(ctypes.addressof(ctypes.c_char.from_buffer(data)), 0, len(data))
    except:
        for i in range(len(data)):
            data[i] = 0


def derive_session_key(sdk_secret: str, app_id: str, device_id: str) -> Tuple[bytes, None]:
    salt = f"evora-session:{app_id}:{device_id}".encode('utf-8')
    secret_bytes = bytearray(sdk_secret.encode('utf-8'))
    
    try:
        derived = hashlib.pbkdf2_hmac(
            'sha256',
            bytes(secret_bytes),
            salt,
            iterations=10000,
            dklen=32
        )
        return derived, None
    finally:
        secure_zero_memory(secret_bytes)


def hmac_sha256(key: bytes, message: str) -> str:
    import hmac
    return hmac.new(key, message.encode('utf-8'), 'sha256').hexdigest()


def generate_box_keypair() -> Tuple[bytes, bytes]:
    private_key = PrivateKey.generate()
    public_key = private_key.public_key
    return bytes(public_key), bytes(private_key)


def generate_signing_keypair() -> Tuple[bytes, bytes]:
    signing_key = SigningKey.generate()
    verify_key = signing_key.verify_key
    return bytes(verify_key), bytes(signing_key)


def encrypt_box(
    plaintext: bytes,
    recipient_public_key: bytes,
    sender_secret_key: bytes
) -> Tuple[bytes, bytes]:
    box = Box(PrivateKey(sender_secret_key), PublicKey(recipient_public_key))
    nonce = secrets.token_bytes(24)
    ciphertext = box.encrypt(plaintext, nonce)
    return nonce, ciphertext.ciphertext


def decrypt_box(
    ciphertext: bytes,
    nonce: bytes,
    sender_public_key: bytes,
    recipient_secret_key: bytes
) -> bytes:
    box = Box(PrivateKey(recipient_secret_key), PublicKey(sender_public_key))
    return box.decrypt(ciphertext, nonce)


def sign_detached(message: bytes, secret_key: bytes) -> bytes:
    signing_key = SigningKey(secret_key)
    signed = signing_key.sign(message)
    return signed.signature


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encrypt_request_body(
    json_body: dict,
    server_public_key_b64: str,
    client_public_key: bytes,
    client_secret_key: bytes,
    kid: Optional[str] = None
) -> dict:
    server_public_key = base64.b64decode(server_public_key_b64)
    plaintext = json.dumps(json_body).encode('utf-8')
    nonce, ciphertext = encrypt_box(plaintext, server_public_key, client_secret_key)
    payload = {
        "v2Encrypted": True,
        "ciphertext": base64.b64encode(ciphertext).decode('ascii'),
        "nonce": base64.b64encode(nonce).decode('ascii'),
        "clientPublicKey": base64.b64encode(client_public_key).decode('ascii'),
    }
    if kid:
        payload["kid"] = kid
    return payload


def decrypt_response_body(
    encrypted_response: dict,
    client_secret_key: bytes,
    server_public_key_b64: str
) -> dict:
    if not encrypted_response.get("v2Encrypted"):
        return encrypted_response
    server_public_key = base64.b64decode(server_public_key_b64)
    ciphertext = base64.b64decode(encrypted_response["ciphertext"])
    nonce = base64.b64decode(encrypted_response["nonce"])
    plaintext = decrypt_box(ciphertext, nonce, server_public_key, client_secret_key)
    return json.loads(plaintext.decode('utf-8'))


def generate_nonce() -> str:
    return secrets.token_hex(16)

def generate_timestamp() -> int:
    return int(time.time())


def create_dpop_token(
    method: str,
    uri: str,
    signing_secret_key: bytes,
    signing_public_key: bytes,
    access_token_hash: Optional[str] = None
) -> str:
    signing_key = SigningKey(signing_secret_key)
    header = {
        "typ": "dpop+jwt",
        "alg": "EdDSA",
        "jwk": {
            "kty": "OKP",
            "crv": "Ed25519",
            "x": base64.urlsafe_b64encode(signing_public_key).rstrip(b'=').decode('ascii')
        }
    }
    payload = {
        "jti": secrets.token_hex(16),
        "htm": method.upper(),
        "htu": uri,
        "iat": int(time.time()),
    }
    if access_token_hash:
        payload["ath"] = access_token_hash
    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).rstrip(b'=').decode('ascii')
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b'=').decode('ascii')
    message = f"{header_b64}.{payload_b64}".encode('utf-8')
    signature = signing_key.sign(message).signature
    signature_b64 = base64.urlsafe_b64encode(signature).rstrip(b'=').decode('ascii')
    return f"{header_b64}.{payload_b64}.{signature_b64}"


def sha256_base64url(data: str) -> str:
    h = hashlib.sha256(data.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(h).rstrip(b'=').decode('ascii')

def generate_hwid() -> str:
    try:
        import uuid
        mac = uuid.getnode()
        combined = f"{mac}-{os.name}-python"
        return hashlib.sha256(combined.encode()).hexdigest()[:32]
    except:
        return secrets.token_hex(16)
