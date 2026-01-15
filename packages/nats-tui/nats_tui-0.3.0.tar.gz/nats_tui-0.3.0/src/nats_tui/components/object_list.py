"""Object list widget for displaying files in an object store."""

import logging

from textual.message import Message
from textual.widgets import Label, ListItem, ListView

from nats_tui.messages import ObjectInfo

logger = logging.getLogger(__name__)


class ObjectList(ListView):
    """List of objects (files) in an object store."""

    class ObjectSelected(Message):
        """Posted when an object is selected."""

        def __init__(self, name: str) -> None:
            super().__init__()
            self.name = name

    def __init__(self) -> None:
        super().__init__(id="object_list")
        self._objects: list[ObjectInfo] = []
        self._store: str = ""
        # Pagination state
        self._total_count: int = 0
        self._offset: int = 0
        self._limit: int = 50

    def set_objects(
        self,
        store: str,
        objects: list[ObjectInfo],
        total_count: int = 0,
        offset: int = 0,
        limit: int = 50,
    ) -> None:
        """Update the object list with pagination.

        Args:
            store: Store name
            objects: List of ObjectInfo for current page
            total_count: Total number of objects in store
            offset: Current offset
            limit: Page size
        """
        logger.debug(
            f"ObjectList.set_objects called: store={store}, objects={len(objects)}, "
            f"total={total_count}, offset={offset}, limit={limit}"
        )
        self._store = store
        self._objects = objects
        self._total_count = total_count
        self._offset = offset
        self._limit = limit
        self.clear()

        # Add pagination header if there are multiple pages
        if total_count > limit:
            start = offset + 1
            end = min(offset + len(objects), total_count)
            page_num = (offset // limit) + 1
            total_pages = (total_count + limit - 1) // limit
            header = f"[dim]Files {start}-{end} of {total_count} (p{page_num}/{total_pages})[/dim]"
            header_item = ListItem(Label(header))
            header_item._object_name = None  # type: ignore
            self.append(header_item)

        for obj in self._objects:
            label = f"  {obj.name}  [{obj.size_str}]"
            logger.debug(f"Adding object item: {label}")
            item = ListItem(Label(label))
            item._object_name = obj.name  # type: ignore
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
                footer_item._object_name = None  # type: ignore
                self.append(footer_item)

        # Ensure the first actual object item is selected after loading
        if objects:
            # Skip header if present
            self.index = 1 if total_count > limit else 0
            logger.debug(f"Set initial object index to {self.index}")

    def clear_objects(self) -> None:
        """Clear all objects from the list."""
        self._objects.clear()
        self._store = ""
        self._total_count = 0
        self._offset = 0
        self.clear()

    def on_focus(self) -> None:
        """Handle focus gained - ensure first object item is highlighted."""
        if self._objects and self.index is None:
            # Skip header if present (when paginated)
            self.index = 1 if self._total_count > self._limit else 0
            logger.debug(f"Focus gained, set index to {self.index}")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle object selection (Enter key)."""
        if event.item and hasattr(event.item, "_object_name") and event.item._object_name:
            logger.debug(f"Object selected (Enter): {event.item._object_name}")
            self.post_message(self.ObjectSelected(event.item._object_name))

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        """Handle object highlight (navigation)."""
        if event.item and hasattr(event.item, "_object_name") and event.item._object_name:
            logger.debug(f"Object highlighted (navigation): {event.item._object_name}")
            self.post_message(self.ObjectSelected(event.item._object_name))

    @property
    def selected_object(self) -> str | None:
        """Get the currently selected object name.

        NOTE: Use this property instead of event item attributes to avoid stale data.
        """
        # Get the actual highlighted item and check its _object_name
        if self.index is not None:
            try:
                items = list(self.children)
                if 0 <= self.index < len(items):
                    item = items[self.index]
                    if hasattr(item, "_object_name") and item._object_name:
                        return item._object_name
            except Exception:
                pass
        return None

    @property
    def store(self) -> str:
        """Get the current store name."""
        return self._store

    @property
    def total_count(self) -> int:
        """Get total number of objects in store."""
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

    def get_object_info(self, name: str) -> ObjectInfo | None:
        """Get an object by name from current page."""
        for obj in self._objects:
            if obj.name == name:
                return obj
        return None
