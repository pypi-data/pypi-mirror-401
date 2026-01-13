"""
Basic example of using the AuthGuard Python SDK.

This demonstrates the typical flow:
1. Initialize session
2. Register device
3. Login/License
4. Use protected endpoints
"""

from authguard import AuthGuardClient

# Replace with your actual app ID
APP_ID = "08cb8404-e78e-4d86-a94a-a7f24a1b559d"

# Optional: For apps with SDK secret enabled
OWNER_ID = None  # "06874c6e-35b9-4e36-8fab-bb0f213f09d6"
SDK_SECRET = None  # "your-sdk-secret"


def main():
    # Initialize client
    client = AuthGuardClient(
        app_id=APP_ID,
        owner_id=OWNER_ID,
        sdk_secret=SDK_SECRET,
        # host="api.evora.lol",  # Default
        # use_https=True,        # Default
    )
    
    print("Initializing session...")
    result = client.init_session()
    if not result.ok:
        print(f"Failed to init session: {result.error}")
        return
    print(f"Session ID: {client.session_id}")
    
    print("\nRegistering device...")
    result = client.ensure_device()
    if not result.ok:
        print(f"Failed to register device: {result.error}")
        return
    print(f"Device ID: {client.device.device_id}")
    print(f"Access token obtained: {bool(client.device.access_token)}")
    
    # Example: Login with username/password
    print("\n--- Login Example ---")
    result = client.login("testuser", "testpassword")
    if result.ok:
        print(f"Login successful!")
        print(f"User data: {result.data}")
    else:
        print(f"Login failed: {result.error}")
    
    # Example: License authentication
    print("\n--- License Example ---")
    result = client.license("XXXX-XXXX-XXXX-XXXX")
    if result.ok:
        print(f"License valid!")
        print(f"License data: {result.data}")
    else:
        print(f"License invalid: {result.error}")
    
    # Example: Check session
    print("\n--- Check Session ---")
    result = client.check()
    if result.ok:
        print(f"Session valid: {result.data}")
    else:
        print(f"Session check failed: {result.error}")
    
    # Example: Get variable
    print("\n--- Get Variable ---")
    result = client.get_var("version")
    if result.ok:
        print(f"Variable value: {result.data.get('value')}")
    else:
        print(f"Get var failed: {result.error}")
    
    # Example: Send heartbeat
    print("\n--- Heartbeat ---")
    result = client.heartbeat()
    if result.ok:
        print("Heartbeat sent successfully")
    else:
        print(f"Heartbeat failed: {result.error}")
    
    # Example: Log event
    print("\n--- Log Event ---")
    result = client.log("app_started", {"version": "1.0.0"})
    if result.ok:
        print("Event logged successfully")
    else:
        print(f"Log failed: {result.error}")


if __name__ == "__main__":
    main()
