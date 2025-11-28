"""Carriers/Vendors menu and actions for the TUI."""

from typing import TYPE_CHECKING

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

from .menu import Menu, MenuItem

if TYPE_CHECKING:
    from ..client import SipNavClient


def list_switch_carriers(client: "SipNavClient", console: Console) -> None:
    """List switch carriers from the API with pagination support."""
    current_page = 1
    per_page = 15  # Items per page for readable display

    while True:
        console.print(f"\n[bold cyan]Fetching carriers (page {current_page})...[/bold cyan]\n")

        try:
            response = client.carriers.list(per_page=per_page, page=current_page)
            
            # Handle different API response structures
            # Could be: {"data": {"data": [...], "total": N, ...}} 
            # Or: {"data": [...]}
            # Or: [...]
            if isinstance(response, list):
                # Direct list response
                carriers = response
                total = len(carriers)
                last_page = 1
                current = 1
                from_item = 1 if carriers else 0
                to_item = len(carriers)
            elif isinstance(response, dict):
                data = response.get("data", response)
                if isinstance(data, list):
                    # {"data": [...]} format
                    carriers = data
                    total = len(carriers)
                    last_page = 1
                    current = 1
                    from_item = 1 if carriers else 0
                    to_item = len(carriers)
                elif isinstance(data, dict):
                    # {"data": {"data": [...], "total": N, ...}} format (Laravel pagination)
                    carriers = data.get("data", [])
                    total = data.get("total", len(carriers))
                    last_page = data.get("last_page", 1)
                    current = data.get("current_page", current_page)
                    from_item = data.get("from", 1)
                    to_item = data.get("to", len(carriers))
                else:
                    carriers = []
                    total = 0
                    last_page = 1
                    current = 1
                    from_item = 0
                    to_item = 0
            else:
                carriers = []
                total = 0
                last_page = 1
                current = 1
                from_item = 0
                to_item = 0

            if not carriers:
                console.print("[yellow]No carriers found.[/yellow]")
                return

            # Build table
            table = Table(
                title=f"Switch Carriers (Page {current}/{last_page})",
                show_header=True,
                header_style="bold magenta"
            )
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
            console.print(
                f"\n[dim]Showing {from_item}-{to_item} of {total} carrier(s) | "
                f"Page {current}/{last_page}[/dim]"
            )

            # Pagination navigation
            nav_options = []
            if current > 1:
                nav_options.append("[P] Previous")
            if current < last_page:
                nav_options.append("[N] Next")
            nav_options.append("[G] Go to page")
            nav_options.append("[Q] Back to menu")

            console.print(f"\n[bold]{' | '.join(nav_options)}[/bold]")
            choice = Prompt.ask("[bold green]Select[/bold green]").strip().lower()

            if choice == "n" and current < last_page:
                current_page += 1
            elif choice == "p" and current > 1:
                current_page -= 1
            elif choice == "g":
                try:
                    page_num = int(Prompt.ask(f"[bold]Enter page number (1-{last_page})[/bold]"))
                    if 1 <= page_num <= last_page:
                        current_page = page_num
                    else:
                        console.print(f"[red]Invalid page. Enter 1-{last_page}.[/red]")
                except ValueError:
                    console.print("[red]Invalid input. Enter a number.[/red]")
            elif choice == "q" or choice == "":
                return
            else:
                console.print("[red]Invalid option.[/red]")

        except Exception as e:
            console.print(f"[bold red]Error fetching carriers:[/bold red] {e}")
            return


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
