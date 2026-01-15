"""Key/Value key list widget."""

import logging

from textual.message import Message
from textual.widgets import Label, ListItem, ListView

from nats_tui.messages import KVEntry

logger = logging.getLogger(__name__)


class KVKeyList(ListView):
    """List of keys in a KV bucket."""

    class KeySelected(Message):
        """Posted when a key is selected."""

        def __init__(self, key: str) -> None:
            super().__init__()
            self.key = key

    def __init__(self) -> None:
        super().__init__(id="kv_key_list")
        self._keys: list[str] = []
        self._bucket: str = ""
        self._entries: dict[str, KVEntry] = {}  # Cache of loaded entries
        # Pagination state
        self._total_count: int = 0
        self._offset: int = 0
        self._limit: int = 50

    def set_keys(
        self,
        bucket: str,
        keys: list[str],
        total_count: int = 0,
        offset: int = 0,
        limit: int = 50,
    ) -> None:
        """Update the key list with pagination.

        Args:
            bucket: Bucket name
            keys: List of key names for current page
            total_count: Total number of keys in bucket
            offset: Current offset
            limit: Page size
        """
        logger.debug(
            f"KVKeyList.set_keys called: bucket={bucket}, keys={len(keys)}, "
            f"total={total_count}, offset={offset}, limit={limit}"
        )
        self._bucket = bucket
        self._keys = keys  # Already sorted by adapter
        self._total_count = total_count
        self._offset = offset
        self._limit = limit
        self._entries.clear()
        self.clear()

        # Add pagination header if there are multiple pages
        if total_count > limit:
            start = offset + 1
            end = min(offset + len(keys), total_count)
            page_num = (offset // limit) + 1
            total_pages = (total_count + limit - 1) // limit
            header = f"[dim]Keys {start}-{end} of {total_count} (p{page_num}/{total_pages})[/dim]"
            header_item = ListItem(Label(header))
            header_item._key_name = None  # type: ignore
            self.append(header_item)

        for key in self._keys:
            label = f"  {key}"
            logger.debug(f"Adding key item: {label}")
            item = ListItem(Label(label))
            item._key_name = key  # type: ignore
            self.append(item)

        # Add pagination footer hint if there are multiple pages
        if total_count > limit:
            has_prev = offset > 0
            has_next = offset + limit < total_count
            hints = []
            if has_prev:
                hints.append("p=prev")
            if has_next:
                hints.append("n=next")
            if hints:
                footer = f"[dim]{' | '.join(hints)}[/dim]"
                footer_item = ListItem(Label(footer))
                footer_item._key_name = None  # type: ignore
                self.append(footer_item)

        # Ensure the first actual key item is selected after loading
        if keys:
            # Skip header if present
            self.index = 1 if total_count > limit else 0
            logger.debug(f"Set initial key index to {self.index}")

    def update_entry(self, entry: KVEntry) -> None:
        """Update a key entry with loaded data.

        Args:
            entry: Loaded KVEntry
        """
        self._entries[entry.key] = entry

        # Update the list item display
        for i, key in enumerate(self._keys):
            if key == entry.key:
                # Get size info
                size_str = f"{entry.size:,} B" if entry.size < 1024 else f"{entry.size / 1024:.1f} KB"
                label = f"  {key}  [{size_str}] rev:{entry.revision}"

                # Replace the item
                item = ListItem(Label(label))
                item._key_name = key  # type: ignore
                # Note: ListView doesn't support direct item replacement
                # so we skip visual update for now - the detail view will show info
                break

    def clear_keys(self) -> None:
        """Clear all keys from the list."""
        self._keys.clear()
        self._bucket = ""
        self._entries.clear()
        self.clear()

    def on_focus(self) -> None:
        """Handle focus gained - ensure first key item is highlighted."""
        if self._keys and self.index is None:
            # Skip header if present (when paginated)
            self.index = 1 if self._total_count > self._limit else 0
            logger.debug(f"Focus gained, set index to {self.index}")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle key selection (Enter key)."""
        if event.item and hasattr(event.item, "_key_name") and event.item._key_name:
            logger.debug(f"Key selected (Enter): {event.item._key_name}")
            self.post_message(self.KeySelected(event.item._key_name))

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        """Handle key highlight (navigation)."""
        if event.item and hasattr(event.item, "_key_name") and event.item._key_name:
            logger.debug(f"Key highlighted (navigation): {event.item._key_name}")
            self.post_message(self.KeySelected(event.item._key_name))

    @property
    def selected_key(self) -> str | None:
        """Get the currently selected key."""
        # Get the actual highlighted item and check its _key_name
        if self.index is not None:
            try:
                items = list(self.children)
                if 0 <= self.index < len(items):
                    item = items[self.index]
                    if hasattr(item, "_key_name") and item._key_name:
                        return item._key_name
            except Exception:
                pass
        return None

    @property
    def bucket(self) -> str:
        """Get the current bucket name."""
        return self._bucket

    @property
    def total_count(self) -> int:
        """Get total number of keys in bucket."""
        return self._total_count

    @property
    def offset(self) -> int:
        """Get current pagination offset."""
        return self._offset

    @property
    def limit(self) -> int:
        """Get pagination page size."""
        return self._limit

    @property
    def has_next_page(self) -> bool:
        """Check if there's a next page."""
        return self._offset + self._limit < self._total_count

    @property
    def has_prev_page(self) -> bool:
        """Check if there's a previous page."""
        return self._offset > 0

    def get_entry(self, key: str) -> KVEntry | None:
        """Get a cached entry by key."""
        return self._entries.get(key)
