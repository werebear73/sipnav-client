# Quick Start: Semantic Versioning

## Current Version
```bash
python -m setuptools_scm
# Output: 0.1.0
```

## Creating a New Release

### 1. Make your changes
```bash
# Edit files, add features, fix bugs
git add .
git commit -m "Add new statistics endpoint"
```

### 2. Tag the release
```bash
# Bug fix (0.1.0 → 0.1.1)
git tag v0.1.1

# New feature (0.1.1 → 0.2.0)
git tag v0.2.0

# Breaking change (0.2.0 → 1.0.0)
git tag v1.0.0
```

### 3. Push to remote (when ready)
```bash
git push origin main
git push origin v0.2.0
```

## Version in Python Code

```python
import sipnav
print(sipnav.__version__)  # Output: 0.1.0
```

## Building the Package

```bash
# Install build tools
pip install build

# Build the package (version auto-detected from git tag)
python -m build

# The dist/ folder will contain:
# - sipnav_client-0.1.0-py3-none-any.whl
# - sipnav-client-0.1.0.tar.gz
```

## Development Version

Between tagged releases, the version includes extra info:
```bash
# Make a commit after tagging v0.1.0
git commit -m "Work in progress"

# Check version
python -m setuptools_scm
# Output: 0.1.1.dev1+g14de1f0

# This means:
# - Next version will be 0.1.1
# - 1 commit since last tag
# - Git hash: 14de1f0
```

## Common Commands

```bash
# View current version
python -m setuptools_scm

# View all tags
git tag -l

# View latest tag
git describe --tags

# Delete a tag (if needed)
git tag -d v0.1.0

# Install package in development mode
pip install -e .
```

## Troubleshooting

**Version shows "0.0.0.dev0"**
- You need to create a git tag: `git tag v0.1.0`

**Version not updating after new tag**
- Reinstall: `pip install -e .`

**"Not a git repository" error**
- Initialize git: `git init`
- Commit files: `git add . && git commit -m "Initial commit"`
- Tag version: `git tag v0.1.0`

## See Also

- Full guide: [VERSIONING.md](VERSIONING.md)
- Changelog: [CHANGELOG.md](CHANGELOG.md)
- Semantic Versioning: https://semver.org/
