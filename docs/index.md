# Welcome to SIPNAV Python Client

A comprehensive Python client library for interacting with the SIPNAV (Blue Dragon Network) REST API.

## Overview

The SIPNAV Python Client provides an easy-to-use interface for managing telecommunications infrastructure including accounts, carriers, companies, CDR records, call restrictions, and more through the Blue Dragon Network API.

## Key Features

- **Resource-based API** - Organized endpoints into logical resource classes
- **Automatic Authentication** - Bearer token authentication with platform support
- **Comprehensive Coverage** - All major API endpoints implemented
- **Error Handling** - Custom exceptions for different error types
- **Type Hints** - Full type annotations for better IDE support
- **Retry Logic** - Automatic retries with exponential backoff
- **Context Manager** - Automatic resource cleanup

## Quick Start

### Installation

```bash
pip install sipnav-client
```

Or install from source:

```bash
git clone https://github.com/yourusername/sipnav-client.git
cd sipnav-client
pip install -e .
```

### Basic Example

```python
from sipnav import SipNavClient

# Method 1: Using bearer token
client = SipNavClient(
    api_key="your_bearer_token",
    platform_id=1  # Optional
)

# Method 2: Using username and password
client = SipNavClient(
    username="your_username",
    password="your_password",
    platform_id=1  # Optional
)

# List accounts
accounts = client.accounts.list(per_page=10)
print(f"Total accounts: {accounts['data']['total']}")

# Get specific account
account = client.accounts.get(account_id=12)
print(account['data']['account_name'])

# Search CDR records
cdr_results = client.cdr.search(
    start_date="2025-01-01 00:00:00",
    end_time="2025-01-31 23:59:59",
    account_id="12"
)
```

## Getting an API Token

You can authenticate in two ways:

### Method 1: Direct Authentication (Recommended)

The simplest way is to pass your credentials directly:

```python
from sipnav import SipNavClient

# Client automatically obtains and uses the bearer token
client = SipNavClient(
    username="your_username",
    password="your_password"
)
```

### Method 2: Manual Token Retrieval

Alternatively, you can manually retrieve the token:

```python
from sipnav import SipNavClient

# Create client with temporary credentials
temp_client = SipNavClient(api_key="temp")

# Login to get token
response = temp_client.auth.login(
    username="your_username",
    password="your_password"
)

# Extract token
token = response["data"]["token"]

# Use token for subsequent requests
client = SipNavClient(api_key=token)
```

## Next Steps

- [Installation Guide](installation.md) - Detailed installation instructions
- [User Guide](user-guide/index.md) - Complete guide to using the library
- [API Reference](api-reference/index.md) - Full API documentation
- [Examples](examples/index.md) - Code examples and use cases

## Support

- **Email**: krice@sipnavigator.com
- **API Documentation**: [https://api.bluedragonnetwork.com/api/documentation](https://api.bluedragonnetwork.com/api/documentation)
- **Issues**: [GitHub Issues](https://github.com/yourusername/sipnav-client/issues)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/yourusername/sipnav-client/blob/main/LICENSE) file for details.
