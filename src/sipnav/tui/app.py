"""Main TUI application for SIPNAV Client."""

import os
import sys
from getpass import getpass
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt

from ..client import SipNavClient
from ..exceptions import AuthenticationError, SipNavException
from .menu import Menu, MenuItem
from .carriers_menu import create_carriers_menu


console = Console()


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def display_menu(menu: Menu) -> None:
    """Display a menu with numbered options."""
    console.print(Panel(f"[bold cyan]{menu.title}[/bold cyan]", expand=False))
    console.print()

    for idx, item in enumerate(menu.items, start=1):
        hotkey_hint = f" [{item.hotkey}]" if item.hotkey else ""
        submenu_hint = " →" if item.submenu else ""
        console.print(f"  [bold]{idx}.[/bold] {item.label}{hotkey_hint}{submenu_hint}")

    console.print()
    if menu.parent:
        console.print("  [dim]B. Back to previous menu[/dim]")
    console.print("  [dim]Q. Quit[/dim]")
    console.print()


def get_user_choice(menu: Menu) -> Optional[MenuItem]:
    """Get user's menu selection."""
    choice = Prompt.ask("[bold green]Select an option[/bold green]").strip()

    if not choice:
        return None

    # Check for quit
    if choice.lower() == "q":
        return MenuItem(label="__quit__", action=lambda: None)

    # Check for back
    if choice.lower() == "b" and menu.parent:
        return MenuItem(label="__back__", action=lambda: None)

    # Check for hotkey
    item = menu.get_item_by_hotkey(choice)
    if item:
        return item

    # Check for numeric selection
    try:
        index = int(choice)
        return menu.get_item_by_index(index)
    except ValueError:
        pass

    console.print("[red]Invalid selection. Please try again.[/red]")
    return None


def login_prompt(base_url: str = "https://api.bluedragonnetwork.com") -> Optional[SipNavClient]:
    """Prompt for credentials and return authenticated client."""
    console.print(Panel("[bold cyan]SIPNAV Login[/bold cyan]", expand=False))
    console.print()

    # Check environment variables first
    env_username = os.environ.get("SIPNAV_USERNAME")
    env_password = os.environ.get("SIPNAV_PASSWORD")
    env_api_key = os.environ.get("SIPNAV_API_KEY")

    if env_api_key:
        console.print("[dim]Using API key from environment...[/dim]")
        try:
            client = SipNavClient(api_key=env_api_key, base_url=base_url)
            console.print("[green]✓ Authenticated successfully![/green]\n")
            return client
        except AuthenticationError as e:
            console.print(f"[red]Authentication failed: {e}[/red]\n")

    if env_username and env_password:
        console.print("[dim]Using credentials from environment...[/dim]")
        try:
            client = SipNavClient(username=env_username, password=env_password, base_url=base_url)
            console.print("[green]✓ Authenticated successfully![/green]\n")
            return client
        except AuthenticationError as e:
            console.print(f"[red]Authentication failed: {e}[/red]\n")

    # Prompt for credentials
    username = Prompt.ask("[bold]Username[/bold]")
    password = getpass("Password: ")

    try:
        client = SipNavClient(username=username, password=password, base_url=base_url)
        console.print("[green]✓ Authenticated successfully![/green]\n")
        return client
    except AuthenticationError as e:
        console.print(f"[red]Authentication failed: {e}[/red]")
        return None
    except SipNavException as e:
        console.print(f"[red]Connection error: {e}[/red]")
        return None


def create_main_menu(client: SipNavClient) -> Menu:
    """Create the main menu after login."""
    main_menu = Menu(title="SIPNAV Main Menu")

    # Add Carriers/Vendors submenu
    carriers_menu = create_carriers_menu(client, console)
    main_menu.add_submenu("Carriers / Vendors", carriers_menu, hotkey="C")

    return main_menu


def run_menu_loop(menu: Menu) -> bool:
    """Run the menu loop. Returns False to quit, True to continue."""
    while True:
        display_menu(menu)
        item = get_user_choice(menu)

        if item is None:
            continue

        if item.label == "__quit__":
            return False

        if item.label == "__back__" and menu.parent:
            return True  # Go back to parent menu

        if item.submenu:
            # Enter submenu
            if not run_menu_loop(item.submenu):
                return False  # Quit propagated up
        elif item.action:
            # Execute action
            try:
                item.action()
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")

            # Pause after action
            Prompt.ask("\n[dim]Press Enter to continue...[/dim]")


def run_tui(base_url: str = "https://api.bluedragonnetwork.com") -> None:
    """Run the SIPNAV TUI application."""
    clear_screen()

    console.print(
        Panel(
            "[bold blue]SIPNAV Client TUI[/bold blue]\n"
            "[dim]Terminal User Interface for SIPNAV API[/dim]",
            expand=False,
        )
    )
    console.print()

    # Login
    client = login_prompt(base_url)
    if not client:
        console.print("[yellow]Exiting...[/yellow]")
        sys.exit(1)

    # Create and run main menu
    main_menu = create_main_menu(client)

    try:
        run_menu_loop(main_menu)
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted. Exiting...[/yellow]")
    finally:
        client.close()
        console.print("[dim]Goodbye![/dim]")


if __name__ == "__main__":
    run_tui()
