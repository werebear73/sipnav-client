"""Carriers/Vendors menu and actions for the TUI."""

from typing import TYPE_CHECKING, List, Dict, Any
import math

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

from .menu import Menu, MenuItem

if TYPE_CHECKING:
    from ..client import SipNavClient


def list_switch_carriers(client: "SipNavClient", console: Console) -> None:
    """List switch carriers from the API with client-side pagination."""
    per_page = 15  # Items per page for readable display

    console.print("\n[bold cyan]Fetching carriers...[/bold cyan]\n")

    try:
        # Fetch all carriers (API returns all in one response)
        response = client.carriers.list(per_page=1000)
        
        # Extract carriers list from response
        if isinstance(response, list):
            all_carriers = response
        elif isinstance(response, dict):
            data = response.get("data", response)
            if isinstance(data, list):
                all_carriers = data
            elif isinstance(data, dict):
                all_carriers = data.get("data", [])
            else:
                all_carriers = []
        else:
            all_carriers = []

        if not all_carriers:
            console.print("[yellow]No carriers found.[/yellow]")
            return

        # Calculate pagination
        total = len(all_carriers)
        last_page = math.ceil(total / per_page)
        current_page = 1

        while True:
            # Get current page slice
            start_idx = (current_page - 1) * per_page
            end_idx = start_idx + per_page
            carriers = all_carriers[start_idx:end_idx]
            
            from_item = start_idx + 1
            to_item = min(end_idx, total)

            # Build table
            table = Table(
                title=f"Switch Carriers (Page {current_page}/{last_page})",
                show_header=True,
                header_style="bold magenta"
            )
            table.add_column("ID", style="cyan", justify="right")
            table.add_column("Name", style="green", no_wrap=True)
            table.add_column("Enabled", style="yellow", justify="center")
            table.add_column("Group", style="blue", justify="right")

            for carrier in carriers:
                carrier_id = str(carrier.get("carrier_id", "N/A"))
                name = carrier.get("carrier_name", "N/A")
                enabled = "Yes" if carrier.get("enabled") == 2 else "No" if carrier.get("enabled") is not None else "N/A"
                group_id = str(carrier.get("group_id", "N/A"))
                table.add_row(carrier_id, str(name), enabled, group_id)

            console.print(table)
            console.print(
                f"\n[dim]Showing {from_item}-{to_item} of {total} carrier(s) | "
                f"Page {current_page}/{last_page}[/dim]"
            )

            # Pagination navigation
            nav_options = []
            if current_page > 1:
                nav_options.append("[P] Previous")
            if current_page < last_page:
                nav_options.append("[N] Next")
            if last_page > 1:
                nav_options.append("[G] Go to page")
            nav_options.append("[Q] Back to menu")

            console.print(f"\n[bold]{' | '.join(nav_options)}[/bold]")
            choice = Prompt.ask("[bold green]Select[/bold green]").strip().lower()

            if choice == "n" and current_page < last_page:
                current_page += 1
            elif choice == "p" and current_page > 1:
                current_page -= 1
            elif choice == "g" and last_page > 1:
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
