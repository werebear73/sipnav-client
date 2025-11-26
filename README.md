# SIPNAV Python Client

A comprehensive Python client library for interacting with the SIPNAV (Blue Dragon Network) REST API. This library provides easy-to-use interfaces for managing accounts, carriers, companies, CDR records, call restrictions, rate decks, and more.

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from sipnav import SipNavClient

# Method 1: Initialize with username and password (recommended)
client = SipNavClient(
    username="your_username",
    password="your_password",
    platform_id=1  # Optional: for multi-platform users
)

# Method 2: Initialize with Bearer token
client = SipNavClient(
    api_key="your_bearer_token_here",
    platform_id=1  # Optional: for multi-platform users
)

# List accounts
accounts = client.accounts.list(per_page=10)
print(f"Total accounts: {accounts['data']['total']}")

# Get specific account
account = client.accounts.get(account_id=12)
print(account['data'])

# Search CDR records
cdr_results = client.cdr.search(
    start_date="2025-01-01 00:00:00",
    end_time="2025-01-31 23:59:59",
    account_id="12"
)

# LRN Lookup
lrn_info = client.lrn.lookup("5125551212")
```

## Authentication

You can authenticate using either username/password or a bearer token:

### Direct Authentication (Recommended)
```python
# Client automatically handles authentication
client = SipNavClient(
    username="your_username",
    password="your_password"
)
```

### Using Bearer Token
```python
# If you already have a token
client = SipNavClient(api_key="your_bearer_token")
```

### Manual Token Retrieval
```python
# Manually get the token
temp_client = SipNavClient(api_key="temp")
login_response = temp_client.auth.login(username="your_username", password="your_password")
token = login_response["data"]["token"]

# Use token for subsequent requests
client = SipNavClient(api_key=token)
client = SipNavClient(api_key=token)
```

## Features

### Resource Classes

The client provides organized resource classes for different API endpoints:

- **`client.accounts`** - Account management (list, get, create, update)
- **`client.carriers`** - Carrier management (list, get, create, update)
- **`client.companies`** - Company management (list, get, create, update, get_balance)
- **`client.cdr`** - CDR search and retrieval
- **`client.call_restrictions`** - Call restriction management (list, create, update, disable)
- **`client.auth`** - Authentication (login, logout, password reset, OTP)
- **`client.lrn`** - LRN lookup
- **`client.rate_decks`** - Rate deck management (account and carrier)

### Key Features

- ✅ **Easy-to-use Python interface** for SIPNAV REST API
- ✅ **Automatic Bearer token authentication** with platform_id support
- ✅ **Comprehensive error handling** (AuthenticationError, APIError, SipNavException)
- ✅ **Automatic retries** with exponential backoff for failed requests
- ✅ **Type hints** for better IDE support and code completion
- ✅ **Context manager support** for automatic resource cleanup
- ✅ **Detailed logging** and debugging support

## API Coverage

### Accounts
```python
# List accounts
accounts = client.accounts.list(per_page=100, company_id=5)

# Get account by ID
account = client.accounts.get(account_id=12)

# Create account
new_account = client.accounts.create(account_data={
    "account_name": "Test Account",
    "customer_id": 2
})

# Update account
updated = client.accounts.update(account_id=12, account_data={
    "account_name": "Updated Name"
})

# Get carriers for account
carriers = client.accounts.get_carriers(account_id=12)
```

### Carriers
```python
# List carriers
carriers = client.carriers.list(per_page=10)

# Get carrier by ID
carrier = client.carriers.get(carrier_id=2)

# Get accounts for carrier
accounts = client.carriers.get_accounts(carrier_id=2)
```

### Companies
```python
# List companies
companies = client.companies.list(per_page=10)

# Get company by ID
company = client.companies.get(company_id=5)

# Get company balance
balance = client.companies.get_balance(company_id=5)

# Get company names
names = client.companies.get_names()
```

### CDR (Call Detail Records)
```python
# Search CDR records
results = client.cdr.search(
    start_date="2025-01-01 00:00:00",
    end_time="2025-01-31 23:59:59",
    account_id="12",
    src_number="5125551212",
    dst_number="5125559999",
    min_duration=30,
    limit=1000
)
```

### Call Restrictions
```python
# List call restrictions
restrictions = client.call_restrictions.list(
    account_id=12,
    carrier_id=2,
    per_page=100
)

# Create call restriction
restriction = client.call_restrictions.create(
    priority=10,
    carrier_id=2,
    account_id=12,
    dst_number=5125551212,
    restriction_start="2025-01-01 00:00:00",
    restriction_end="2025-12-31 23:59:59",
    note="Block this number"
)

# Disable restriction
client.call_restrictions.disable(restriction_id=123)
```

### LRN Lookup
```python
# Lookup LRN for phone number
result = client.lrn.lookup("5125551212")
print(result['data'])
```

### Rate Decks
```python
# Get account rate decks
rate_decks = client.rate_decks.get_account_rate_decks(
    account_id=12,
    local=1  # 1 for local, 0 for international
)

# Get carrier rate decks
carrier_decks = client.rate_decks.get_carrier_rate_decks(carrier_id=2)

# Check processing status
status = client.rate_decks.check_rate_deck_status(filename="rates.csv")
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
    print(f"General error: {e}")
```

## Advanced Usage

### Using Context Manager
```python
with SipNavClient(api_key="token") as client:
    accounts = client.accounts.list()
    # Connection automatically closed
```

### Custom Base URL and Timeout
```python
client = SipNavClient(
    api_key="token",
    base_url="https://custom-api.example.com",
    timeout=60,  # 60 seconds
    max_retries=5
)
```

## Development

### Setup Development Environment

```bash
# Install with development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=sipnav --cov-report=term-missing
```

### Code Formatting

```bash
# Format code with black
black src/ tests/

# Check with flake8
flake8 src/ tests/

# Type checking with mypy
mypy src/
```

## API Documentation

Full API documentation is available at:
- Swagger UI: https://api.bluedragonnetwork.com/api/documentation
- OpenAPI Spec: https://api.bluedragonnetwork.com/docs?api-docs.json

## Support

For issues and questions:
- **Maintainer**: Sam Ware (samuel@waretech.services)
- **Organization**: [Waretech Services](https://waretech.services)
- **GitHub Issues**: [https://github.com/werebear73/sipnav-client/issues](https://github.com/werebear73/sipnav-client/issues)
- **API Documentation**: https://api.bluedragonnetwork.com/api/documentation

## Versioning

This project uses [Semantic Versioning](https://semver.org/) (SemVer). Versions are automatically managed using `setuptools_scm` based on git tags.

## License

This project is licensed under the GNU General Public License v3.0. See the
`LICENSE` file in the repository for the full license text.

**Current version:**
```bash
python -m setuptools_scm
```

**Check version in Python:**
```python
import sipnav
print(sipnav.__version__)
```

**Creating a release:**
```bash
git tag v0.2.0  # New version tag
git push origin v0.2.0
```

See [VERSIONING.md](VERSIONING.md) for detailed information about version management.

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit your changes: `git commit -m "Add new feature"`
4. Push to the branch: `git push origin feature/new-feature`
5. Submit a pull request

Please update [CHANGELOG.md](CHANGELOG.md) with your changes.

## License

MIT
