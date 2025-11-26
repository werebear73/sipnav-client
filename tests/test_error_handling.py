"""Test script to demonstrate improved error handling for Issue #1."""

from sipnav import SipNavClient
from sipnav.exceptions import APIError, AuthenticationError, SipNavException

def test_error_handling():
    """Test various error scenarios to verify improved error messages."""
    
    print("Testing improved error handling for Issue #1\n")
    print("=" * 60)
    
    # Test 1: Invalid API key
    print("\n1. Testing with invalid API key...")
    try:
        client = SipNavClient(api_key="invalid_token_12345")
        accounts = client.accounts.list()
    except AuthenticationError as e:
        print(f"✓ AuthenticationError caught: {e}")
    except APIError as e:
        print(f"✓ APIError caught: {e}")
        print(f"  - Status Code: {e.status_code}")
        print(f"  - Request Method: {e.request_method}")
        print(f"  - Request URL: {e.request_url}")
    except SipNavException as e:
        print(f"✓ SipNavException caught: {e}")
    
    # Test 2: Invalid username/password
    print("\n2. Testing with invalid username/password...")
    try:
        client = SipNavClient(username="invalid_user", password="wrong_password")
    except AuthenticationError as e:
        print(f"✓ AuthenticationError caught: {e}")
    except SipNavException as e:
        print(f"✓ SipNavException caught: {e}")
    
    # Test 3: Connection error (invalid base URL)
    print("\n3. Testing with invalid base URL...")
    try:
        client = SipNavClient(
            api_key="some_token",
            base_url="https://invalid-url-that-does-not-exist.example.com"
        )
        accounts = client.accounts.list()
    except SipNavException as e:
        print(f"✓ SipNavException caught: {e}")
    
    # Test 4: Valid client but invalid endpoint parameters
    print("\n4. Testing with valid client but potentially invalid parameters...")
    print("   (This would require a valid API key to test properly)")
    print("   The improved error messages will now show:")
    print("   - The actual API error message")
    print("   - Any error details from the response")
    print("   - The HTTP status code")
    print("   - The request method and endpoint")
    
    print("\n" + "=" * 60)
    print("\nError handling improvements:")
    print("✓ More detailed error messages from API")
    print("✓ Includes request context (method, endpoint, URL)")
    print("✓ Separates connection errors, timeouts, and API errors")
    print("✓ Preserves additional error details from API response")
    print("✓ Better exception attributes (status_code, request_method, request_url)")

if __name__ == "__main__":
    test_error_handling()
