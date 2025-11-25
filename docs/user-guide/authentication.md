# Authentication

Learn how to authenticate with the SIPNAV API and manage tokens.

## Overview

The SIPNAV API uses **Bearer token authentication**. You need to:

1. Login with username/password to get a token
2. Use the token for all subsequent API requests
3. Optionally specify a `platform_id` for multi-platform users

## Getting a Token

### Method 1: Direct Authentication (Recommended)

The simplest way to authenticate is by providing your username and password directly to the client:

```python
from sipnav import SipNavClient

# Client automatically obtains and uses the bearer token
client = SipNavClient(
    username="your_username",
    password="your_password",
    platform_id=1  # Optional
)

# Make API calls immediately
accounts = client.accounts.list()
```

The client will:
1. Authenticate with the `/api/login` endpoint
2. Extract the bearer token from the response
3. Use the token for all subsequent API requests

### Method 2: Using Existing Bearer Token

If you already have a bearer token:

```python
from sipnav import SipNavClient

# Use existing token
client = SipNavClient(api_key="your_bearer_token")

# Make API calls
accounts = client.accounts.list()
```

### Method 3: Manual Login

You can also manually retrieve the token using the authentication resource:

```python
from sipnav import SipNavClient

# Create a temporary client
temp_client = SipNavClient(api_key="placeholder")

# Login to get token
response = temp_client.auth.login(
    username="your_username",
    password="your_password"
)

# Extract the token
token = response["data"]["token"]
username = response["data"]["username"]

print(f"Successfully logged in as: {username}")
print(f"Token: {token}")

# Create authenticated client
client = SipNavClient(api_key=token)
```

## Platform ID

If you have access to multiple platforms, specify the `platform_id`:

```python
client = SipNavClient(
    api_key=token,
    platform_id=1  # Your platform ID
)
```

The `platform_id` is automatically added to all API requests.

## Token Management

### Storing Tokens Securely

**Don't hardcode tokens in your code!** Use environment variables:

```python
import os
from sipnav import SipNavClient

token = os.getenv("SIPNAV_API_TOKEN")
if not token:
    raise ValueError("SIPNAV_API_TOKEN environment variable not set")

client = SipNavClient(api_key=token)
```

Set the environment variable:

```bash
# Windows (PowerShell)
$env:SIPNAV_API_TOKEN="your_token_here"

# Linux/Mac
export SIPNAV_API_TOKEN="your_token_here"
```

### Using Configuration Files

Store credentials in a config file (don't commit to git!):

```python
import json
from sipnav import SipNavClient

# Load from config file
with open("config.json") as f:
    config = json.load(f)

client = SipNavClient(
    api_key=config["api_token"],
    platform_id=config.get("platform_id")
)
```

`config.json`:
```json
{
    "api_token": "your_token_here",
    "platform_id": 1
}
```

Add `config.json` to `.gitignore`!

## Logout

```python
# Logout current user
response = client.auth.logout()
print(response["message"])
```

## Password Management

### Send Password Reset Email

```python
# Send reset email
response = client.auth.send_password_reset_email(
    username="user@example.com",
    platform_id=1  # Optional, for sipnav admins
)
print(response["message"])
```

### Reset Password

After receiving the reset email with encrypted user ID and temp password:

```python
response = client.auth.reset_password(
    encrypted_user="encrypted_string_from_email",
    temp_password="temporary_password_from_email",
    new_password="your_new_secure_password",
    confirm_password="your_new_secure_password"
)
print(response["message"])
```

## Two-Factor Authentication (2FA)

### Verify OTP Code

If 2FA is enabled, verify the one-time code:

```python
response = client.auth.verify_otp(
    encrypted_user="encrypted_user_id",
    two_factor_code=123456
)

# Extract token
token = response["data"]["token"]
username = response["data"]["username"]
```

## Proxy User Sessions

### Start Proxy Session

System/platform admins can proxy as another user:

```python
# Start proxy session for user ID 5
response = client.auth.start_proxy(user_id=5)

proxy_token = response["token"]
proxy_username = response["name"]

# Create client as proxied user
proxy_client = SipNavClient(api_key=proxy_token)
```

### Stop Proxy Session

```python
# Stop proxy and return to original user
response = client.auth.stop_proxy()

original_token = response["token"]
original_username = response["name"]
```

## Authentication Errors

Handle authentication errors properly:

```python
from sipnav import SipNavClient
from sipnav.exceptions import AuthenticationError

try:
    client = SipNavClient(api_key="invalid_token")
    accounts = client.accounts.list()
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
    # Re-authenticate
    # token = get_new_token()
```

## Best Practices

### 1. Store Tokens Securely
```python
# ❌ Bad - hardcoded
client = SipNavClient(api_key="abc123token")

# ✅ Good - environment variable
import os
client = SipNavClient(api_key=os.getenv("SIPNAV_API_TOKEN"))
```

### 2. Handle Token Expiration
```python
from sipnav.exceptions import AuthenticationError

def make_api_call():
    try:
        return client.accounts.list()
    except AuthenticationError:
        # Token expired, re-authenticate
        new_token = login_and_get_token()
        client.api_key = new_token
        return client.accounts.list()
```

### 3. Use Context Manager
```python
# Automatically closes connection
with SipNavClient(api_key=token) as client:
    accounts = client.accounts.list()
```

### 4. Validate Credentials Early
```python
def validate_credentials(username, password):
    try:
        temp_client = SipNavClient(api_key="temp")
        response = temp_client.auth.login(username, password)
        return response["data"]["token"]
    except AuthenticationError:
        return None

token = validate_credentials("user", "pass")
if token:
    client = SipNavClient(api_key=token)
else:
    print("Invalid credentials")
```

## Complete Example

```python
import os
from sipnav import SipNavClient
from sipnav.exceptions import AuthenticationError, SipNavException

def get_authenticated_client():
    """Get authenticated client using credentials or token."""
    # Try token from environment first
    token = os.getenv("SIPNAV_API_TOKEN")
    
    if token:
        return SipNavClient(api_key=token, platform_id=1)
    
    # Otherwise, use username/password
    username = os.getenv("SIPNAV_USERNAME")
    password = os.getenv("SIPNAV_PASSWORD")
    
    if username and password:
        return SipNavClient(
            username=username,
            password=password,
            platform_id=1
        )
    
    # Prompt for credentials if not in environment
    username = input("Username: ")
    password = input("Password: ")
    
    try:
        return SipNavClient(
            username=username,
            password=password,
            platform_id=1
        )
    except AuthenticationError as e:
        print(f"Authentication failed: {e}")
        raise

# Usage
try:
    client = get_authenticated_client()
    accounts = client.accounts.list(per_page=5)
    print(f"Found {accounts['data']['total']} accounts")
except SipNavException as e:
    print(f"Error: {e}")
```

## Next Steps

- [Quick Start](quickstart.md) - Get started using the client
