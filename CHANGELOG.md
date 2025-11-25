# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Username/password authentication support in SipNavClient constructor
- Automatic bearer token retrieval via `/api/login` endpoint
- MkDocs Material documentation site with awesome-pages plugin
- Comprehensive documentation structure (user guides, API reference, examples)
- GitHub repository integration
- Enhanced .gitignore for Python and VS Code

### Changed
- Updated all documentation to show both authentication methods
- Made `api_key` parameter optional when username/password provided

## [0.1.0] - 2025-11-25

### Added
- Initial implementation of SIPNAV Python client library
- Resource classes for major API endpoints:
  - Accounts management (list, get, create, update)
  - Carriers management (list, get, create, update)
  - Companies management (list, get, create, update, balance)
  - CDR search functionality
  - Call restrictions management
  - Authentication (login, logout, password reset, OTP)
  - LRN lookup
  - Rate deck management
- Automatic Bearer token authentication
- Platform ID support for multi-platform users
- Comprehensive error handling (AuthenticationError, APIError, SipNavException)
- Automatic retry logic with exponential backoff
- Context manager support for resource cleanup
- Type hints throughout the codebase
- Unit tests with pytest
- Development tools setup (black, flake8, mypy)
- Semantic versioning with setuptools_scm

---

## Guidelines for Updating

### Version Types

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** in case of vulnerabilities

### When to Update

Update this file:
1. When adding a new feature
2. When fixing a bug
3. Before creating a release tag
4. When making breaking changes

### Format

```markdown
## [Version] - YYYY-MM-DD

### Added
- New feature description

### Fixed
- Bug fix description

### Changed
- Change description
```

### Example Entry

```markdown
## [0.2.0] - 2025-11-26

### Added
- New `statistics` resource for usage statistics endpoints
- Support for proxy user management
- Batch operations for call restrictions

### Changed
- Improved error messages for authentication failures
- Updated rate limiting handling

### Fixed
- Fixed issue with pagination in carrier list
- Corrected date format in CDR search

### Deprecated
- `client.get()` method - use resource-specific methods instead
```
