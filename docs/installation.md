# Installation

## Requirements

- Python 3.8 or higher
- pip (Python package installer)
- Git (for development installation)

## Stable Release

Install from PyPI (when published):

```bash
pip install sipnav-client
```

## Development Installation

For the latest development version:

```bash
# Clone the repository
git clone https://github.com/yourusername/sipnav-client.git
cd sipnav-client

# Install in development mode
pip install -e .
```

## With Development Tools

To install with development dependencies (for contributing):

```bash
pip install -e ".[dev]"
```

This includes:
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `black` - Code formatter
- `flake8` - Linting
- `mypy` - Type checking
- `types-requests` - Type stubs for requests

## Verify Installation

After installation, verify it works:

```python
import sipnav
print(sipnav.__version__)
```

Or check installed packages:

```bash
pip show sipnav-client
```

## Virtual Environment (Recommended)

It's recommended to use a virtual environment:

### Using venv

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install package
pip install sipnav-client
```

### Using conda

```bash
# Create environment
conda create -n sipnav python=3.11

# Activate
conda activate sipnav

# Install package
pip install sipnav-client
```

## Upgrading

To upgrade to the latest version:

```bash
pip install --upgrade sipnav-client
```

## Uninstalling

To remove the package:

```bash
pip uninstall sipnav-client
```

## Dependencies

The package automatically installs these dependencies:

- **requests** (>=2.28.0) - HTTP library
- **urllib3** (>=1.26.0) - HTTP client

## Troubleshooting

### SSL Certificate Errors

If you encounter SSL errors:

```python
import requests
client = SipNavClient(api_key="token")
# Temporarily disable SSL verification (not recommended for production)
client.session.verify = False
```

### Import Errors

If you get import errors after installation:

1. Ensure you're using the correct Python environment
2. Reinstall the package: `pip install --force-reinstall sipnav-client`
3. Check for conflicting packages

### Version Not Found

If `sipnav.__version__` shows `0.0.0.dev0`:

- This means setuptools_scm couldn't detect the version
- For development: Run `pip install -e .` in the git repository
- For production: Install from PyPI

## Next Steps

- [Quick Start Guide](user-guide/quickstart.md)
- [Authentication](user-guide/authentication.md)
