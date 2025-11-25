"""Basic usage examples for the SIPNAV client library."""

import os
from sipnav import SipNavClient
from sipnav.exceptions import SipNavException, AuthenticationError

# Method 1: Initialize with username and password (recommended)
# The client will automatically obtain and use the bearer token
# client = SipNavClient(
#     username="your_username",
#     password="your_password",
#     platform_id=1  # Optional
# )

# Method 2: Initialize with bearer token
# Set these as environment variables for better security
api_key = os.getenv("SIPNAV_API_TOKEN", "your_bearer_token_here")
platform_id = 1  # Optional: specify if you have multiple platforms

client = SipNavClient(api_key=api_key, platform_id=platform_id)

try:
    # Note: If using Method 1 (username/password), you don't need to manually login
    # The client handles authentication automatically
    
    # Example 2: List accounts
    accounts = client.accounts.list(per_page=10)
    print(f"Found {accounts['data']['total']} accounts")
    for account in accounts['data']['data']:
        print(f"  - {account['account_name']} (ID: {account['account_id']})")
    
    # Example 3: Get a specific account
    account_id = 12
    account_details = client.accounts.get(account_id)
    print(f"\nAccount Details: {account_details['data']}")
    
    # Example 4: List companies
    companies = client.companies.list(per_page=10)
    print(f"\nFound {companies['data']['total']} companies")
    
    # Example 5: Search CDR records
    cdr_results = client.cdr.search(
        start_date="2025-01-01 00:00:00",
        end_time="2025-01-31 23:59:59",
        account_id="12",
        limit=100
    )
    print(f"\nCDR Search Results: {cdr_results}")
    
    # Example 6: LRN Lookup
    phone_number = "5125551212"
    lrn_result = client.lrn.lookup(phone_number)
    print(f"\nLRN Lookup for {phone_number}: {lrn_result}")
    
    # Example 7: List carriers
    carriers = client.carriers.list(per_page=10)
    print(f"\nFound {carriers['data']['total']} carriers")
    
    # Example 8: Get call restrictions
    restrictions = client.call_restrictions.list(per_page=50)
    print(f"\nCall Restrictions: {restrictions}")
    
    # Example 9: Using context manager (auto-closes connection)
    with SipNavClient(api_key=api_key) as client:
        companies = client.companies.get_names()
        print(f"\nCompany Names: {companies}")
    
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except SipNavException as e:
    print(f"API Error: {e}")
finally:
    # Close the client connection
    client.close()
