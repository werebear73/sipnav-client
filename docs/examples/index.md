# Examples

Code examples and use cases for the SIPNAV Python Client.

## Available Examples

More examples coming soon!

## Running Examples

All examples are available in the `examples/` directory of the repository:

```bash
# Clone the repository
git clone https://github.com/yourusername/sipnav-client.git
cd sipnav-client/examples

# Run an example
python basic_usage.py
```

## Example Template

Here's a basic template for your scripts:

```python
import os
from sipnav import SipNavClient
from sipnav.exceptions import SipNavException

def main():
    # Get token from environment
    token = os.getenv("SIPNAV_API_TOKEN")
    if not token:
        print("Error: SIPNAV_API_TOKEN environment variable not set")
        return
    
    # Initialize client
    client = SipNavClient(api_key=token, platform_id=1)
    
    try:
        # Your code here
        accounts = client.accounts.list(per_page=5)
        print(f"Total accounts: {accounts['data']['total']}")
        
    except SipNavException as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
```

## Contributing Examples

Have a useful example? Please contribute!

1. Fork the repository
2. Add your example to `examples/`
3. Document it in `docs/examples/`
4. Submit a pull request
