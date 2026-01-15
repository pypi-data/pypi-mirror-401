"""Key/Value bucket list widget."""

import logging

from textual.message import Message
from textual.widgets import Label, ListItem, ListView

from nats_tui.messages import KVBucketInfo

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


class KVBucketList(ListView):
    """List of Key/Value buckets."""

    class BucketSelected(Message):
        """Posted when a bucket is selected."""

        def __init__(self, bucket: KVBucketInfo) -> None:
            super().__init__()
            self.bucket = bucket

    def __init__(self) -> None:
        super().__init__(id="kv_bucket_list")
        self._buckets: list[KVBucketInfo] = []

    def set_buckets(self, buckets: list[KVBucketInfo]) -> None:
        """Update the bucket list.

        Args:
            buckets: List of KVBucketInfo objects
        """
        logger.debug(f"set_buckets called with {len(buckets)} buckets")
        self._buckets = buckets
        self.clear()
        for bucket in buckets:
            storage_icon = "F" if bucket.storage == "file" else "M"
            label = f"[{storage_icon}] {bucket.name} ({bucket.values:,} keys)"
            logger.debug(f"Adding bucket item: {label}")
            item = ListItem(Label(label))
            item._bucket_info = bucket  # type: ignore
            self.append(item)

        # Ensure the first item is selected after loading
        if buckets:
            self.index = 0
            logger.debug(f"Set initial index to 0")

    def clear_buckets(self) -> None:
        """Clear all buckets from the list."""
        self._buckets.clear()
        self.clear()

    def on_focus(self) -> None:
        """Handle focus gained - ensure first item is highlighted."""
        if self._buckets and self.index is None:
            self.index = 0
            logger.debug("Focus gained, set index to 0")

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle bucket selection (Enter key)."""
        if event.item and hasattr(event.item, "_bucket_info"):
            self.post_message(self.BucketSelected(event.item._bucket_info))

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        """Handle bucket highlight (navigation)."""
        if event.item and hasattr(event.item, "_bucket_info"):
            self.post_message(self.BucketSelected(event.item._bucket_info))

    @property
    def selected_bucket(self) -> KVBucketInfo | None:
        """Get the currently selected bucket."""
        if self.index is not None and 0 <= self.index < len(self._buckets):
            return self._buckets[self.index]
        return None
