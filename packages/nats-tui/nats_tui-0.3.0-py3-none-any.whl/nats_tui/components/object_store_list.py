"""Object Store list widget."""

import logging

from textual.message import Message
from textual.widgets import Label, ListItem, ListView

from nats_tui.messages import ObjectStoreInfo

logger = logging.getLogger(__name__)


def _format_bytes(num_bytes: int) -> str:
    """Format bytes into human-readable string."""
    if num_bytes < 0:
        return "unlimited"
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} PB"


class ObjectStoreList(ListView):
    """List of Object Stores."""

    class StoreSelected(Message):
        """Posted when an object store is selected."""

        def __init__(self, store: ObjectStoreInfo) -> None:
            super().__init__()
            self.store = store

    def __init__(self) -> None:
        super().__init__(id="object_store_list")
        self._stores: list[ObjectStoreInfo] = []

    def set_stores(self, stores: list[ObjectStoreInfo]) -> None:
        """Update the object store list.

        Args:
            stores: List of ObjectStoreInfo objects
        """
        logger.debug(f"set_stores called with {len(stores)} stores")
        self._stores = stores
        self.clear()
        for store in stores:
            storage_icon = "F" if store.storage == "file" else "M"
            size_str = _format_bytes(store.size)
            label = f"[{storage_icon}] {store.name} ({store.objects:,} files, {size_str})"
            logger.debug(f"Adding store item: {label}")
            item = ListItem(Label(label))
            item._store_info = store  # type: ignore
            self.append(item)

        # Ensure the first item is selected after loading
        if stores:
            self.index = 0
            logger.debug("Set initial index to 0")

    def clear_stores(self) -> None:
        """Clear all stores from the list."""
        self._stores.clear()
        self.clear()

    def on_focus(self) -> None:
        """Handle focus gained - ensure first item is highlighted."""
        if self._stores and self.index is None:
            self.index = 0
            logger.debug("Focus gained, set index to 0")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle store selection (Enter key)."""
        if event.item and hasattr(event.item, "_store_info"):
            self.post_message(self.StoreSelected(event.item._store_info))

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        """Handle store highlight (navigation)."""
        if event.item and hasattr(event.item, "_store_info"):
            self.post_message(self.StoreSelected(event.item._store_info))

    @property
    def selected_store(self) -> ObjectStoreInfo | None:
        """Get the currently selected store.

        NOTE: Use this property instead of event item attributes to avoid stale data.
        """
        if self.index is not None and 0 <= self.index < len(self._stores):
            return self._stores[self.index]
        return None
