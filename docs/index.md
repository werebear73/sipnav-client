# Welcome to SIPNAV Python Client

A Python client library for the SIPNAV (Blue Dragon Network) REST API.

## Overview

The SIPNAV Python Client provides an easy-to-use interface for managing telecommunications infrastructure including accounts, carriers, companies, CDR records, call restrictions, and more through the Blue Dragon Network API.

## Key Features

- **Resource-based API** — Organized endpoints into logical resource classes
- **Multiple Auth Methods** — Username/password or Bearer token authentication
- **Terminal UI** — Interactive TUI for exploring the API
- **Comprehensive Coverage** — All major API endpoints implemented
- **Error Handling** — Custom exceptions with detailed error messages
- **Type Hints** — Full type annotations for IDE support
- **Retry Logic** — Automatic retries with exponential backoff

## Quick Start

```python
from sipnav import SipNavClient

client = SipNavClient(
    username="your_username",
    password="your_password"
)

# List carriers
carriers = client.carriers.list(per_page=10)

# Search CDR
cdr = client.cdr.search(
    start_date="2025-01-01 00:00:00",
    end_time="2025-01-31 23:59:59"
)
```

## Documentation

### Getting Started

| Guide | Description |
|-------|-------------|
| [Quick Start](user-guide/quickstart.md) | Installation and first steps |
| [Authentication](user-guide/authentication.md) | Auth methods and token handling |

### Using the Library

| Guide | Description |
|-------|-------------|
| [API Coverage](user-guide/api-coverage.md) | Detailed examples for all resources |
| [Error Handling](user-guide/error-handling.md) | Exception types and handling patterns |
| [TUI Guide](user-guide/tui.md) | Terminal User Interface usage |

### Reference

| Section | Description |
|---------|-------------|
| [API Reference](api-reference/index.md) | Full API documentation |
| [Examples](examples/index.md) | Code examples and recipes |
| [Roadmap](roadmap.md) | Planned features and improvements |

## Terminal UI

Run the interactive TUI:

```bash
sipnav-tui
```

Or as a module:

```bash
python -m sipnav.tui.app
```

## Support

- **Maintainer**: Sam Ware (samuel@waretech.services)
- **Organization**: [Waretech Services](https://waretech.services)
- **GitHub Issues**: [Report an issue](https://github.com/werebear73/sipnav-client/issues)
- **API Documentation**: [SIPNAV API Docs](https://api.bluedragonnetwork.com/api/documentation)

## License

This project is licensed under the GNU General Public License v3.0 — see the [LICENSE](https://github.com/werebear73/sipnav-client/blob/master/LICENSE) file for details.
