"""Carriers/Vendors menu and actions for the TUI."""

from typing import TYPE_CHECKING

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .menu import Menu, MenuItem

if TYPE_CHECKING:
    from ..client import SipNavClient


def list_switch_carriers(client: "SipNavClient", console: Console) -> None:
    """List all switch carriers from the API."""
    console.print("\n[bold cyan]Fetching carriers...[/bold cyan]\n")

    try:
        response = client.carriers.list(per_page=100)
        carriers = response.get("data", {}).get("data", [])

        if not carriers:
            console.print("[yellow]No carriers found.[/yellow]")
            return

        table = Table(title="Switch Carriers", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="cyan", justify="right")
        table.add_column("Name", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Type", style="blue")

        for carrier in carriers:
            carrier_id = str(carrier.get("id", "N/A"))
            name = carrier.get("name", "N/A")
            status = carrier.get("status", "N/A")
            carrier_type = carrier.get("type", "N/A")
            table.add_row(carrier_id, name, str(status), str(carrier_type))

        console.print(table)
        console.print(f"\n[dim]Total: {len(carriers)} carrier(s)[/dim]")

    except Exception as e:
        console.print(f"[bold red]Error fetching carriers:[/bold red] {e}")


def create_carriers_menu(client: "SipNavClient", console: Console) -> Menu:
    """Create the Carriers/Vendors sub-menu."""
    menu = Menu(title="Carriers / Vendors")

    menu.add_item(
        MenuItem(
            label="List Switch Carriers",
            action=lambda: list_switch_carriers(client, console),
            hotkey="L",
        )
    )

    return menu
