# Quick Start

Get up and running with the SIPNAV Python Client in 5 minutes.

## Installation

```bash
pip install sipnav-client
```

## Authentication

You can authenticate using either username/password or a bearer token.

### Method 1: Username and Password (Recommended)

The easiest way is to provide your credentials directly:

```python
from sipnav import SipNavClient

# Client automatically handles authentication
client = SipNavClient(
    username="your_username",
    password="your_password",
    platform_id=1  # Optional
)
```

### Method 2: Bearer Token

If you already have a bearer token:

```python
from sipnav import SipNavClient

# Use existing token
client = SipNavClient(
    api_key="your_bearer_token",
    platform_id=1  # Optional
)
```

### Method 3: Manual Token Retrieval

To manually obtain a token:

```python
from sipnav import SipNavClient

# Login to get token
temp_client = SipNavClient(api_key="placeholder")
response = temp_client.auth.login(
    username="your_username",
    password="your_password"
)

token = response["data"]["token"]
print(f"Your token: {token}")

# Use the token
client = SipNavClient(api_key=token)
```

## Basic Operations

### List Accounts

```python
# Get first 10 accounts
accounts = client.accounts.list(per_page=10)

print(f"Total accounts: {accounts['data']['total']}")
for account in accounts['data']['data']:
    print(f"- {account['account_name']} (ID: {account['account_id']})")
```

### Get Account Details

```python
# Get specific account
account = client.accounts.get(account_id=12)
print(account['data'])
```

### Search CDR Records

```python
# Search call records
results = client.cdr.search(
    start_date="2025-01-01 00:00:00",
    end_time="2025-01-31 23:59:59",
    account_id="12",
    limit=100
)
print(f"Found {len(results['data'])} records")
```

### LRN Lookup

```python
# Lookup local routing number
result = client.lrn.lookup("5125551212")
print(result['data'])
```

### List Companies

```python
# Get companies
companies = client.companies.list(per_page=10)
for company in companies['data']['data']:
    print(f"- {company['customer_name']}")
```

## Using Context Manager

For automatic cleanup:

```python
from sipnav import SipNavClient

with SipNavClient(api_key="your_token") as client:
    accounts = client.accounts.list(per_page=5)
    print(accounts['data']['total'])
# Connection automatically closed
```

## Error Handling

```python
from sipnav import SipNavClient
from sipnav.exceptions import AuthenticationError, APIError, SipNavException

try:
    client = SipNavClient(api_key="invalid_token")
    accounts = client.accounts.list()
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except APIError as e:
    print(f"API error: {e} (Status: {e.status_code})")
except SipNavException as e:
    print(f"Error: {e}")
```

## Complete Example

```python
from sipnav import SipNavClient
from sipnav.exceptions import SipNavException

def main():
    # Initialize client
    client = SipNavClient(
        api_key="your_bearer_token",
        platform_id=1
    )
    
    try:
        # List accounts
        print("=== Accounts ===")
        accounts = client.accounts.list(per_page=5)
        for account in accounts['data']['data']:
            print(f"- {account['account_name']} (ID: {account['account_id']})")
        
        # List carriers
        print("\n=== Carriers ===")
        carriers = client.carriers.list(per_page=5)
        for carrier in carriers['data']['data']:
            print(f"- {carrier['carrier_name']} (ID: {carrier['carrier_id']})")
        
        # Get company balance
        print("\n=== Company Balance ===")
        balance = client.companies.get_balance(company_id=2)
        print(f"Balance: ${balance['data']['balanceamount']}")
        
        # LRN Lookup
        print("\n=== LRN Lookup ===")
        lrn = client.lrn.lookup("5125551212")
        print(f"LRN Info: {lrn['data']}")
        
    except SipNavException as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
```

## Next Steps

- [Authentication Guide](authentication.md) - Detailed authentication information
- [API Reference](../api-reference/index.md) - Full API documentation
