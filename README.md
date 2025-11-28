# SIPNAV Python Client

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A Python client library for the SIPNAV (Blue Dragon Network) REST API.

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from sipnav import SipNavClient

# Authenticate with username/password
client = SipNavClient(
    username="your_username",
    password="your_password"
)

# List carriers
carriers = client.carriers.list(per_page=10)

# Search CDR records
cdr = client.cdr.search(
    start_date="2025-01-01 00:00:00",
    end_time="2025-01-31 23:59:59"
)
```

## Features

- ✅ Username/password and Bearer token authentication
- ✅ Resource classes: Accounts, Carriers, Companies, CDR, Call Restrictions, LRN, Rate Decks
- ✅ Automatic retries with exponential backoff
- ✅ Comprehensive error handling
- ✅ Terminal User Interface (TUI) for interactive use
- ✅ Type hints and context manager support

## Terminal UI

```bash
sipnav-tui
# or
python -m sipnav.tui.app
```

## Documentation

Full documentation is available in the `docs/` folder:

| Guide | Description |
|-------|-------------|
| [Quick Start](docs/user-guide/quickstart.md) | Get up and running quickly |
| [Authentication](docs/user-guide/authentication.md) | Auth methods and token handling |
| [TUI Guide](docs/user-guide/tui.md) | Terminal User Interface usage |
| [Error Handling](docs/user-guide/error-handling.md) | Exception types and handling |
| [API Reference](docs/api-reference/index.md) | Full API documentation |
| [Examples](docs/examples/index.md) | Code examples and recipes |

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Lint and format
black src/ tests/
flake8 src/ tests/
mypy src/
```

## Support

- **Maintainer**: Sam Ware (samuel@waretech.services)
- **Organization**: [Waretech Services](https://waretech.services)
- **Issues**: [GitHub Issues](https://github.com/werebear73/sipnav-client/issues)
- **API Docs**: [SIPNAV API Documentation](https://api.bluedragonnetwork.com/api/documentation)

## License

GNU General Public License v3.0 — see [LICENSE](LICENSE).
