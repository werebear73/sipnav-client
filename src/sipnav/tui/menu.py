"""Menu classes for building TUI menus."""

from dataclasses import dataclass, field
from typing import Callable, List, Optional, Any


@dataclass
class MenuItem:
    """A single menu item with a label, optional hotkey, and action."""

    label: str
    action: Optional[Callable[[], Any]] = None
    hotkey: Optional[str] = None
    submenu: Optional["Menu"] = None

    def __post_init__(self) -> None:
        if self.action is None and self.submenu is None:
            raise ValueError("MenuItem must have either an action or a submenu")

    @property
    def display_label(self) -> str:
        """Return label with hotkey hint if present."""
        if self.hotkey:
            return f"[{self.hotkey}] {self.label}"
        return self.label


@dataclass
class Menu:
    """A menu containing multiple MenuItems."""

    title: str
    items: List[MenuItem] = field(default_factory=list)
    parent: Optional["Menu"] = None

    def add_item(self, item: MenuItem) -> None:
        """Add a menu item."""
        self.items.append(item)

    def add_submenu(self, label: str, submenu: "Menu", hotkey: Optional[str] = None) -> None:
        """Add a submenu as a menu item."""
        submenu.parent = self
        self.items.append(MenuItem(label=label, submenu=submenu, hotkey=hotkey))

    def get_item_by_hotkey(self, hotkey: str) -> Optional[MenuItem]:
        """Find a menu item by its hotkey."""
        for item in self.items:
            if item.hotkey and item.hotkey.lower() == hotkey.lower():
                return item
        return None

    def get_item_by_index(self, index: int) -> Optional[MenuItem]:
        """Get a menu item by its 1-based index."""
        if 1 <= index <= len(self.items):
            return self.items[index - 1]
        return None
