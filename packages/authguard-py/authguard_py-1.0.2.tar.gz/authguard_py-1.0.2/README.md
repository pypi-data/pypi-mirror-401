# AuthGuard Python SDK

Python SDK for the AuthGuard v2 API with NaCl box encryption.

## Features

- Full v2 API support with encrypted request/response bodies
- NaCl box encryption (Curve25519 + XSalsa20-Poly1305)
- DPoP (Proof-of-Possession) token support
- Automatic token refresh
- Device registration and session management
- Optional SDK secret authentication (for developer apps)
- Anti-debug report endpoints

## Installation

```bash
pip install authguard-py
```

Or install from source:
```bash
pip install -r requirements.txt
```

## Quick Start

```python
from authguard import AuthGuardClient

# Initialize client
client = AuthGuardClient(
    app_id="your-app-id",
    # Optional: for apps with SDK secret enabled
    owner_id="developer-user-id",
    sdk_secret="your-sdk-secret"
)

# Initialize session and device
client.init_session()
client.ensure_device()

# Login
result = client.login("username", "password")
if result.ok:
    print("Logged in!")
    print(f"User: {result.data.get('username')}")

# Or use license key
result = client.license("XXXX-XXXX-XXXX-XXXX")

# Check session validity
result = client.check()

# Get app variable
result = client.get_var("my_variable")

# Send heartbeat
result = client.heartbeat()

# Log event
client.log("user_action", {"detail": "something happened"})
```

## Configuration Options

```python
client = AuthGuardClient(
    app_id="your-app-id",
    host="api.evora.lol",       # API host (default: api.evora.lol)
    port=443,                    # API port (default: 443)
    use_https=True,              # Use HTTPS (default: True)
    owner_id=None,               # Developer ID for SDK auth
    sdk_secret=None,             # SDK secret for developer auth
    hwid=None,                   # Custom HWID (auto-generated if None)
)
```

## API Reference

### Session Management

- `init_session()` - Initialize app session
- `ensure_device()` - Register/refresh device credentials
- `ensure_access_token()` - Get valid access token (auto-refreshes)

### Authentication

- `login(username, password)` - Authenticate with username/password
- `register(username, password, email=None, key=None)` - Create new account
- `license(license_key)` - Authenticate with license key
- `upgrade(license_key)` - Upgrade account with license key

### Session Operations

- `check()` - Verify session is valid
- `heartbeat()` - Send heartbeat (keep session alive)
- `get_var(name)` - Get application variable
- `log(action, data=None)` - Log an event

### Advanced

- `call_protected(path, data)` - Make authenticated API call
- `call_bootstrap(path, data)` - Make bootstrap API call (no auth)

## Security Notes

- All request bodies are encrypted on the wire using NaCl box
- Device credentials are stored locally (consider encrypting at rest)
- The SDK automatically handles token refresh
- DPoP tokens prove possession of device key

## License

MIT
