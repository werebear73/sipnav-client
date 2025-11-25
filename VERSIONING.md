# Semantic Versioning Guide

This project uses **semantic versioning** (SemVer) with automatic version management via `setuptools_scm`.

## Version Format

Versions follow the pattern: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes (incompatible API changes)
- **MINOR**: New features (backward-compatible)
- **PATCH**: Bug fixes (backward-compatible)

## How It Works

Versions are automatically determined from Git tags. `setuptools_scm` reads the Git history and generates the version number.

### Version Sources

1. **Tagged releases**: `git tag v1.2.3` → version `1.2.3`
2. **Development versions**: Between tags → version `1.2.4.dev5+g1234567`
3. **No tags**: Version `0.0.0.dev0`

## Creating a Release

### 1. Commit your changes
```bash
git add .
git commit -m "Add new feature"
```

### 2. Create a version tag
```bash
# For a new feature (bump MINOR)
git tag v0.2.0

# For a bug fix (bump PATCH)
git tag v0.1.1

# For breaking changes (bump MAJOR)
git tag v1.0.0
```

### 3. Push the tag
```bash
git push origin v0.2.0
```

### 4. Build and publish
```bash
python -m build
python -m twine upload dist/*
```

## Checking Current Version

### From Python
```python
import sipnav
print(sipnav.__version__)
```

### From Command Line
```bash
# After installing in development mode
pip show sipnav-client

# Or using setuptools_scm directly
python -m setuptools_scm
```

## Development Versions

Between releases, the version automatically includes:
- Number of commits since last tag
- Short git commit hash
- "dev" indicator

Example: `0.2.1.dev3+g1a2b3c4`

This means:
- Last tagged version was `0.2.0`
- Next version will be `0.2.1`
- 3 commits since last tag
- Current commit hash: `1a2b3c4`

## Best Practices

### When to Bump Versions

**PATCH (0.1.X)**: 
- Bug fixes
- Documentation updates
- Internal refactoring
- Performance improvements (no API changes)

**MINOR (0.X.0)**:
- New features
- New API endpoints
- New resource methods
- Deprecating features (not removing)

**MAJOR (X.0.0)**:
- Breaking API changes
- Removing deprecated features
- Changing method signatures
- Renaming core classes/methods

### Pre-release Versions

For alpha/beta/rc releases:
```bash
git tag v1.0.0-alpha.1
git tag v1.0.0-beta.1
git tag v1.0.0-rc.1
```

### Versioning Workflow

```bash
# Start work on new feature
git checkout -b feature/new-endpoint

# Make changes and commit
git add .
git commit -m "Add new endpoint for statistics"

# Merge to main
git checkout main
git merge feature/new-endpoint

# Tag the release (new feature = MINOR bump)
git tag v0.2.0
git push origin main
git push origin v0.2.0

# Version 0.2.0 is now available
```

## Version File

The version is automatically written to `src/sipnav/_version.py` during build. **Do not** commit this file to git - it's generated automatically.

Add to `.gitignore`:
```
src/sipnav/_version.py
```

## Troubleshooting

### "No version found"
- Ensure you're in a git repository: `git status`
- Check for tags: `git tag -l`
- Create an initial tag: `git tag v0.1.0`

### Version not updating
- Ensure you've committed your changes
- Check if tag was created: `git describe --tags`
- Reinstall in development mode: `pip install -e .`

### Build fails
- Ensure setuptools_scm is installed: `pip install setuptools_scm`
- Check git is available: `git --version`

## Examples

```bash
# Initial release
git tag v0.1.0
# Version: 0.1.0

# Add commits, no new tag
git commit -m "Work in progress"
# Version: 0.1.1.dev1+g5f6a7b8

# Tag bug fix release
git tag v0.1.1
# Version: 0.1.1

# Tag feature release
git tag v0.2.0
# Version: 0.2.0

# Tag breaking change
git tag v1.0.0
# Version: 1.0.0
```

## CI/CD Integration

In your CI/CD pipeline:

```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    tags:
      - 'v*'
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Required for setuptools_scm
      - name: Build package
        run: python -m build
      - name: Publish to PyPI
        run: python -m twine upload dist/*
```

## References

- [Semantic Versioning 2.0.0](https://semver.org/)
- [setuptools_scm documentation](https://setuptools-scm.readthedocs.io/)
- [PEP 440 - Version Identification](https://peps.python.org/pep-0440/)
