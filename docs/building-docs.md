# Building Documentation

This guide explains how to build and serve the SIPNAV Python Client documentation.

## Prerequisites

Install documentation dependencies:

```bash
pip install -e ".[docs]"
```

This installs:
- `mkdocs` - Documentation site generator
- `mkdocs-material` - Material theme for MkDocs
- `mkdocstrings` - API documentation generator
- `pymdown-extensions` - Markdown extensions

## Building Documentation

### Serve Locally

To preview documentation with live reload:

```bash
mkdocs serve
```

Then open http://127.0.0.1:8000 in your browser.

### Build Static Site

To build the static HTML site:

```bash
mkdocs build
```

The site will be generated in the `site/` directory.

## Documentation Structure

```
docs/
├── index.md                  # Homepage
├── installation.md           # Installation guide
├── user-guide/              # User guides
│   ├── index.md
│   ├── quickstart.md
│   ├── authentication.md
│   └── ...
├── api-reference/           # API documentation
│   ├── index.md
│   ├── client.md
│   └── resources/
├── examples/                # Code examples
│   ├── index.md
│   └── ...
└── stylesheets/            # Custom CSS
    └── extra.css
```

## Writing Documentation

### Markdown Files

Documentation is written in Markdown with extensions:

```markdown
# Page Title

## Section

Regular text with **bold** and *italic*.

### Code Examples

\`\`\`python
from sipnav import SipNavClient
client = SipNavClient(api_key="token")
\`\`\`

### Admonitions

!!! note
    This is a note.

!!! warning
    This is a warning.

!!! tip
    This is a tip.
```

### API Documentation

Use mkdocstrings to auto-generate API docs from docstrings:

```markdown
::: sipnav.SipNavClient
    options:
      show_root_heading: true
      show_source: true
```

### Code Tabs

Show code in multiple languages or examples:

```markdown
=== "Python"
    \`\`\`python
    client = SipNavClient(api_key="token")
    \`\`\`

=== "JSON Response"
    \`\`\`json
    {"success": true, "data": {}}
    \`\`\`
```

## MkDocs Configuration

The `mkdocs.yml` file configures:

- Site metadata (name, description, URLs)
- Theme settings (Material theme with dark mode)
- Navigation structure
- Plugins (search, mkdocstrings)
- Markdown extensions

### Key Sections

**Theme Configuration:**
```yaml
theme:
  name: material
  palette:
    - scheme: default  # Light mode
    - scheme: slate    # Dark mode
  features:
    - navigation.tabs
    - navigation.sections
    - search.suggest
    - content.code.copy
```

**Navigation:**
```yaml
nav:
  - Home: index.md
  - Installation: installation.md
  - User Guide:
    - user-guide/index.md
    - Quick Start: user-guide/quickstart.md
```

## Deploying Documentation

### GitHub Pages

Deploy to GitHub Pages:

```bash
# Build and deploy
mkdocs gh-deploy
```

This:
1. Builds the site
2. Pushes to `gh-pages` branch
3. Makes it available at `https://yourusername.github.io/sipnav-client/`

### Custom Domain

To use a custom domain:

1. Add a `CNAME` file to `docs/`:
   ```
   docs.sipnav.com
   ```

2. Configure DNS to point to GitHub Pages

3. Deploy:
   ```bash
   mkdocs gh-deploy
   ```

### Other Hosting

Deploy the `site/` directory to any static hosting:

```bash
# Build
mkdocs build

# Upload site/ directory to your host
rsync -avz site/ user@host:/var/www/docs/
```

## Live Reload

The `mkdocs serve` command watches for changes:

1. Edit any `.md` file in `docs/`
2. Save the file
3. Browser automatically refreshes

## Custom Styling

Edit `docs/stylesheets/extra.css` for custom styles:

```css
:root {
  --sipnav-primary: #3f51b5;
}

.custom-class {
  color: var(--sipnav-primary);
}
```

Reference in HTML:

```html
<div class="custom-class">Custom styled content</div>
```

## Plugins

### Search

Enabled by default. No configuration needed.

### mkdocstrings

Auto-generates API docs from Python docstrings:

```yaml
plugins:
  - mkdocstrings:
      handlers:
        python:
          options:
            docstring_style: google
            show_source: true
```

Use in Markdown:

```markdown
::: sipnav.SipNavClient
```

## Troubleshooting

### Module not found

If mkdocstrings can't find modules:

```bash
# Install package in development mode
pip install -e .
```

### Port already in use

Change the port:

```bash
mkdocs serve -a localhost:8001
```

### Build errors

Check for:
- Broken links: `mkdocs build --strict`
- Invalid YAML in `mkdocs.yml`
- Missing files referenced in navigation

## Best Practices

1. **Keep it simple** - Use clear, concise language
2. **Show examples** - Include code examples for every feature
3. **Link related pages** - Help users navigate
4. **Update regularly** - Keep docs in sync with code
5. **Test locally** - Preview before deploying

## Next Steps

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
