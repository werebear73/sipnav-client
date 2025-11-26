# Error Handling

Learn how to handle errors and exceptions when using the SIPNAV Python Client.

## Exception Hierarchy

The client uses a structured exception hierarchy:

```
SipNavException (base)
├── AuthenticationError (401 errors, login failures)
└── APIError (other API errors with status codes)
```

## Common Exceptions

### SipNavException

Base exception for all SIPNAV client errors.

```python
from sipnav.exceptions import SipNavException

try:
    client.accounts.list()
except SipNavException as e:
    print(f"Error: {e}")
```

### AuthenticationError

Raised when authentication fails (401 status codes).

```python
from sipnav.exceptions import AuthenticationError

try:
    client = SipNavClient(api_key="invalid_token")
    accounts = client.accounts.list()
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
    # Re-authenticate or prompt for credentials
```

### APIError

Raised when the API returns an error response (4xx, 5xx status codes).

**Attributes:**
- `message`: Error message from the API
- `status_code`: HTTP status code (404, 500, etc.)
- `request_method`: HTTP method used (GET, POST, etc.)
- `request_url`: Full URL that was requested

```python
from sipnav.exceptions import APIError

try:
    account = client.accounts.get(account_id=99999)
except APIError as e:
    print(f"API Error: {e}")
    print(f"Status Code: {e.status_code}")
    print(f"Request: {e.request_method} {e.request_url}")
```

## Error Message Format

The client provides detailed error messages with context:

```
[API Error Message] | Details: [Additional Info] | Request: [METHOD] [ENDPOINT]
```

**Example:**
```
Account not found | Details: Errors: ID does not exist | Request: GET /api/accounts/99999
```

## Handling Specific Error Types

### Connection Errors

```python
from sipnav.exceptions import SipNavException

try:
    client = SipNavClient(
        api_key="token",
        base_url="https://invalid-server.com"
    )
    accounts = client.accounts.list()
except SipNavException as e:
    if "Connection failed" in str(e):
        print("Cannot connect to API server")
        print(f"Error: {e}")
```

### Timeout Errors

```python
try:
    client = SipNavClient(api_key="token", timeout=5)
    large_cdr = client.cdr.search(
        start_date="2020-01-01 00:00:00",
        end_time="2025-12-31 23:59:59"
    )
except SipNavException as e:
    if "timeout" in str(e).lower():
        print("Request took too long")
        # Retry with larger timeout or smaller date range
```

### Invalid Parameters

```python
from sipnav.exceptions import APIError

try:
    account = client.accounts.create(account_data={
        "invalid_field": "value"
    })
except APIError as e:
    if e.status_code == 400:
        print("Invalid request parameters")
        print(f"Details: {e}")
```

### Resource Not Found

```python
from sipnav.exceptions import APIError

try:
    account = client.accounts.get(account_id=99999)
except APIError as e:
    if e.status_code == 404:
        print("Account not found")
```

### Rate Limiting

```python
from sipnav.exceptions import APIError
import time

try:
    for i in range(1000):
        client.accounts.list()
except APIError as e:
    if e.status_code == 429:
        print("Rate limited - waiting before retry")
        time.sleep(60)
        # Retry request
```

## Best Practices

### 1. Catch Specific Exceptions First

```python
from sipnav.exceptions import AuthenticationError, APIError, SipNavException

try:
    accounts = client.accounts.list()
except AuthenticationError as e:
    # Handle authentication issues
    print(f"Auth error: {e}")
except APIError as e:
    # Handle API errors
    print(f"API error: {e} (Status: {e.status_code})")
except SipNavException as e:
    # Handle all other errors
    print(f"Error: {e}")
```

### 2. Log Error Details

```python
import logging
from sipnav.exceptions import APIError

logger = logging.getLogger(__name__)

try:
    account = client.accounts.get(account_id=123)
except APIError as e:
    logger.error(
        f"Failed to get account",
        extra={
            "status_code": e.status_code,
            "method": e.request_method,
            "url": e.request_url,
            "error": str(e)
        }
    )
```

### 3. Implement Retry Logic

```python
from sipnav.exceptions import APIError, SipNavException
import time

def get_account_with_retry(client, account_id, max_retries=3):
    """Get account with automatic retry on transient errors."""
    for attempt in range(max_retries):
        try:
            return client.accounts.get(account_id)
        except APIError as e:
            # Retry on server errors (5xx)
            if e.status_code >= 500:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"Server error, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
            raise
        except SipNavException as e:
            # Retry on connection errors
            if "Connection failed" in str(e) or "timeout" in str(e).lower():
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"Connection error, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
            raise
    
    raise SipNavException(f"Failed after {max_retries} attempts")
```

### 4. Graceful Degradation

```python
from sipnav.exceptions import SipNavException

def get_account_balance_safe(client, company_id):
    """Get account balance with fallback."""
    try:
        balance = client.companies.get_balance(company_id)
        return balance['data']['balanceamount']
    except SipNavException as e:
        print(f"Could not get balance: {e}")
        return 0.0  # Default value
```

### 5. User-Friendly Error Messages

```python
from sipnav.exceptions import AuthenticationError, APIError, SipNavException

def user_friendly_error(e: Exception) -> str:
    """Convert technical error to user-friendly message."""
    if isinstance(e, AuthenticationError):
        return "Your session has expired. Please log in again."
    elif isinstance(e, APIError):
        if e.status_code == 404:
            return "The requested resource was not found."
        elif e.status_code == 403:
            return "You don't have permission to access this resource."
        elif e.status_code >= 500:
            return "The server is experiencing issues. Please try again later."
        else:
            return f"An error occurred: {e}"
    elif isinstance(e, SipNavException):
        if "Connection failed" in str(e):
            return "Cannot connect to the server. Check your internet connection."
        elif "timeout" in str(e).lower():
            return "The request took too long. Please try again."
    return "An unexpected error occurred. Please contact support."

# Usage
try:
    accounts = client.accounts.list()
except Exception as e:
    print(user_friendly_error(e))
```

## Debugging Tips

### Enable Verbose Logging

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('sipnav')
logger.setLevel(logging.DEBUG)
```

### Inspect Full Error Context

```python
from sipnav.exceptions import APIError

try:
    account = client.accounts.get(account_id=123)
except APIError as e:
    print(f"Error Message: {e}")
    print(f"Status Code: {e.status_code}")
    print(f"HTTP Method: {e.request_method}")
    print(f"URL: {e.request_url}")
    print(f"Full Exception: {repr(e)}")
```

### Test Error Handling

```python
def test_error_scenarios():
    """Test various error scenarios."""
    
    # Test 1: Invalid credentials
    try:
        client = SipNavClient(username="wrong", password="wrong")
    except Exception as e:
        print(f"Test 1: {type(e).__name__}: {e}")
    
    # Test 2: Invalid account ID
    try:
        client = SipNavClient(api_key="valid_token")
        client.accounts.get(account_id=99999)
    except Exception as e:
        print(f"Test 2: {type(e).__name__}: {e}")
    
    # Test 3: Connection timeout
    try:
        client = SipNavClient(api_key="valid_token", timeout=0.001)
        client.accounts.list()
    except Exception as e:
        print(f"Test 3: {type(e).__name__}: {e}")

test_error_scenarios()
```

## Common Issues and Solutions

### Issue: Generic Error Messages

**Problem:** Getting "Client does not have 'method' method" error.

**Solution:** This was fixed in v0.3.0. Update to the latest version:
```bash
pip install --upgrade sipnav-client
```

The improved error handling now shows:
- The actual API error message
- HTTP status code
- Request method and endpoint
- Additional error details from the response

### Issue: Authentication Failures

**Problem:** Getting AuthenticationError even with valid credentials.

**Solutions:**
1. Verify credentials are correct
2. Check if the bearer token has expired
3. Ensure platform_id is correct (if using multi-platform)
4. Check base_url is correct for your SIPNAV instance

```python
# Verify connection
from sipnav import SipNavClient
from sipnav.exceptions import AuthenticationError

try:
    client = SipNavClient(
        username="your_username",
        password="your_password",
        base_url="https://your-sipnav-instance.com"
    )
    print("✓ Authentication successful")
except AuthenticationError as e:
    print(f"✗ Authentication failed: {e}")
```

### Issue: Timeout Errors on Large Queries

**Problem:** Requests timing out when searching large CDR datasets.

**Solutions:**
1. Increase timeout value
2. Reduce date range
3. Use pagination

```python
# Solution 1: Increase timeout
client = SipNavClient(api_key="token", timeout=120)

# Solution 2: Smaller date ranges
for month in range(1, 13):
    start = f"2025-{month:02d}-01 00:00:00"
    end = f"2025-{month:02d}-31 23:59:59"
    results = client.cdr.search(start_date=start, end_time=end)

# Solution 3: Use limit parameter
results = client.cdr.search(
    start_date="2025-01-01 00:00:00",
    end_time="2025-12-31 23:59:59",
    limit=1000
)
```

## Next Steps

- [Best Practices](best-practices.md)
- [API Reference](../api-reference/index.md)
- [Examples](../examples/index.md)
