# Terminal User Interface (TUI)

The SIPNAV Client includes an interactive Terminal User Interface for exploring and interacting with the SIPNAV API from the command line.

## Installation

The TUI is included with the main package. Ensure you have the package installed:

```bash
pip install -e .
```

The `rich` library (for enhanced terminal output) is automatically installed as a dependency.

## Running the TUI

### Using the Console Script

```bash
sipnav-tui
```

### Running as a Module

```bash
python -m sipnav.tui.app
```

### Custom Base URL

```python
from sipnav.tui import run_tui

run_tui(base_url="https://custom-api.example.com")
```

## Authentication

The TUI supports multiple authentication methods:

### Environment Variables (Recommended)

Set these environment variables before running the TUI:

```bash
# Windows PowerShell
$env:SIPNAV_USERNAME = "your_username"
$env:SIPNAV_PASSWORD = "your_password"

# Or use an API key
$env:SIPNAV_API_KEY = "your_bearer_token"
```

```bash
# Linux/macOS
export SIPNAV_USERNAME="your_username"
export SIPNAV_PASSWORD="your_password"

# Or use an API key
export SIPNAV_API_KEY="your_bearer_token"
```

### Interactive Login

If no environment variables are set, the TUI will prompt for credentials:

```
┌──────────────┐
│ SIPNAV Login │
└──────────────┘

Username: your_username
Password: ********
✓ Authenticated successfully!
```

## Menu Navigation

### Keyboard Controls

| Key | Action |
|-----|--------|
| `1-9` | Select menu item by number |
| `Hotkey` | Select menu item by hotkey (shown in brackets) |
| `B` | Go back to previous menu |
| `Q` | Quit the application |

### Main Menu

After successful login, you'll see the main menu:

```
┌─────────────────────┐
│ SIPNAV Main Menu    │
└─────────────────────┘

  1. Carriers / Vendors [C] →

  B. Back to previous menu
  Q. Quit
```

## Available Menus

### Carriers / Vendors

Access carrier management functions:

```
┌─────────────────────┐
│ Carriers / Vendors  │
└─────────────────────┘

  1. List Switch Carriers [L]

  B. Back to previous menu
  Q. Quit
```

#### List Switch Carriers

Displays all carriers in a formatted table:

```
                    Switch Carriers
┏━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┓
┃  ID ┃ Name                 ┃ Status  ┃ Type   ┃
┡━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━┩
│   1 │ Primary Carrier      │ active  │ switch │
│   2 │ Backup Carrier       │ active  │ switch │
│   3 │ International Routes │ standby │ switch │
└─────┴──────────────────────┴─────────┴────────┘

Total: 3 carrier(s)
```

## Extending the TUI

### Adding New Menu Items

You can extend the TUI by creating new menu modules:

```python
from sipnav.tui.menu import Menu, MenuItem

def my_custom_action(client, console):
    console.print("Hello from custom action!")

def create_my_menu(client, console):
    menu = Menu(title="My Custom Menu")
    menu.add_item(
        MenuItem(
            label="My Action",
            action=lambda: my_custom_action(client, console),
            hotkey="M",
        )
    )
    return menu
```

### Menu Classes

The TUI provides two core classes for building menus:

#### `MenuItem`

A single menu item with:
- `label` — Display text
- `action` — Callable to execute (optional if submenu provided)
- `hotkey` — Single-character keyboard shortcut
- `submenu` — Nested Menu object (optional if action provided)

#### `Menu`

A container for menu items with:
- `title` — Menu header text
- `items` — List of MenuItem objects
- `parent` — Reference to parent menu (for back navigation)

## Error Handling

The TUI gracefully handles errors:

- **Authentication errors** — Displayed with option to retry
- **API errors** — Shown with detailed error messages
- **Connection errors** — Displayed with troubleshooting hints
- **Keyboard interrupt** (Ctrl+C) — Clean exit with goodbye message

## Troubleshooting

### "sipnav-tui" Command Not Found

Add Python's Scripts directory to your PATH, or run as a module:

```bash
python -m sipnav.tui.app
```

### Authentication Fails with Environment Variables

Verify your environment variables are set correctly:

```powershell
# PowerShell
echo $env:SIPNAV_USERNAME
```

```bash
# Bash
echo $SIPNAV_USERNAME
```

### Rich Output Not Displaying Correctly

Ensure your terminal supports ANSI colors. Most modern terminals (Windows Terminal, iTerm2, GNOME Terminal) work correctly. Legacy Windows Command Prompt may have issues.
