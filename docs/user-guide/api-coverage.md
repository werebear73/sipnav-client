# API Coverage

This page provides detailed examples for all available API resources.

## Accounts

```python
from sipnav import SipNavClient

client = SipNavClient(username="user", password="pass")

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

## Carriers

```python
# List carriers
carriers = client.carriers.list(per_page=10)

# Get carrier by ID
carrier = client.carriers.get(carrier_id=2)

# Get accounts for carrier
accounts = client.carriers.get_accounts(carrier_id=2)
```

## Companies

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

## CDR (Call Detail Records)

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

## Call Restrictions

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

## LRN Lookup

```python
# Lookup LRN for phone number
result = client.lrn.lookup("5125551212")
print(result['data'])
```

## Rate Decks

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

## Authentication Resource

```python
# Login (usually handled automatically)
response = client.auth.login(username="user", password="pass")
token = response["data"]["token"]

# Logout
client.auth.logout()

# Password reset request
client.auth.request_password_reset(email="user@example.com")
```

## Advanced Usage

### Context Manager

```python
with SipNavClient(api_key="token") as client:
    accounts = client.accounts.list()
    # Connection automatically closed
```

### Custom Configuration

```python
client = SipNavClient(
    api_key="token",
    base_url="https://custom-api.example.com",
    timeout=60,  # 60 seconds
    max_retries=5
)
```

### Environment Variables

```python
import os

client = SipNavClient(
    username=os.environ.get("SIPNAV_USERNAME"),
    password=os.environ.get("SIPNAV_PASSWORD")
)
```
