# API Reference

Complete API reference for the SIPNAV Python Client.

## Main Components

- **SipNavClient** - Main client class for API interaction
- **Resources** - Resource classes for different endpoints
- **Exceptions** - Custom exception classes

## Resources

The client provides organized resource classes:

| Resource | Description |
|----------|-------------|
| `client.accounts` | Account management |
| `client.carriers` | Carrier management |
| `client.companies` | Company management |
| `client.cdr` | CDR search |
| `client.call_restrictions` | Call restrictions |
| `client.auth` | Authentication |
| `client.lrn` | LRN lookup |
| `client.rate_decks` | Rate deck management |

## Quick Reference

### Initialize Client

::: sipnav.SipNavClient
    options:
      show_root_heading: false
      show_source: false
      members:
        - __init__

### Common Methods

```python
# GET request
response = client.get("/api/endpoint", params={"key": "value"})

# POST request
response = client.post("/api/endpoint", data={"key": "value"})

# PUT request
response = client.put("/api/endpoint", data={"key": "value"})

# DELETE request
response = client.delete("/api/endpoint")
```

### Context Manager

```python
with SipNavClient(api_key="token") as client:
    accounts = client.accounts.list()
# Automatically closes connection
```

## Exception Hierarchy

```
SipNavException
├── AuthenticationError
└── APIError
```

## Type Hints

All methods include type hints for better IDE support:

```python
from typing import Dict, Any, Optional
from sipnav import SipNavClient

def get_account_info(
    client: SipNavClient,
    account_id: int
) -> Dict[str, Any]:
    return client.accounts.get(account_id)
```

## Response Format

All API responses follow this format:

```json
{
  "success": true,
  "message": "",
  "data": {
    // Response data
  }
}
```

For paginated responses:

```json
{
  "success": true,
  "message": "",
  "data": {
    "current_page": 1,
    "data": [...],
    "total": 100,
    "per_page": 10,
    "last_page": 10
  }
}
```
