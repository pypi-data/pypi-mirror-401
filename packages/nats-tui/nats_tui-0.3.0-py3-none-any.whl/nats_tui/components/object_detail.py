"""Object detail view widget."""

import logging
from datetime import datetime

from textual.containers import VerticalScroll
from textual.widgets import Static

from nats_tui.messages import ObjectInfo

logger = logging.getLogger(__name__)


class ObjectDetail(VerticalScroll):
    """Detail view for an object in an object store."""

    def __init__(self) -> None:
        super().__init__(id="object_detail")
        self._object: ObjectInfo | None = None

    def compose(self):
        """Compose the widget."""
        yield Static("Select an object to view details", id="object_detail_content")

    def set_object(self, obj: ObjectInfo | None) -> None:
        """Update the displayed object info.

        Args:
            obj: ObjectInfo to display, or None to clear
        """
        self._object = obj

        content = self.query_one("#object_detail_content", Static)
        if obj is None:
            content.update("Select an object to view details")
            return

        # Format modification time
        if obj.modified:
            if isinstance(obj.modified, str):
                # Already a string (from API), format for display
                mod_time = obj.modified.replace("T", " ").split("+")[0] + " UTC"
            else:
                # datetime object
                mod_time = obj.modified.strftime("%Y-%m-%d %H:%M:%S UTC")
        else:
            mod_time = "Unknown"

        # Format digest (truncate if long)
        digest = obj.digest if obj.digest else "N/A"
        if len(digest) > 20:
            digest_display = f"{digest[:10]}...{digest[-10:]}"
        else:
            digest_display = digest

        # Build detail display
        lines = [
            f"[bold]Object Details[/bold]",
            "",
            f"[dim]Store:[/dim]     {obj.store}",
            f"[dim]Name:[/dim]      {obj.name}",
            f"[dim]Size:[/dim]      {obj.size_str} ({obj.size:,} bytes)",
            f"[dim]Chunks:[/dim]    {obj.chunks}",
            f"[dim]Modified:[/dim]  {mod_time}",
            f"[dim]Digest:[/dim]    {digest_display}",
            "",
        ]

        if obj.deleted:
            lines.append("[red]Status: DELETED[/red]")
        else:
            lines.append("[green]Status: Active[/green]")

        content.update("\n".join(lines))

    def clear(self) -> None:
        """Clear the detail view."""
        self._object = None
        content = self.query_one("#object_detail_content", Static)
        content.update("Select an object to view details")

    @property
    def current_object(self) -> ObjectInfo | None:
        """Get the currently displayed object."""
        return self._object

    @property
    def object_info(self) -> ObjectInfo | None:
        """Get the currently displayed object (alias for current_object)."""
        return self._object

    @object_info.setter
    def object_info(self, obj: ObjectInfo | None) -> None:
        """Set the object to display.

        Args:
            obj: ObjectInfo to display, or None to clear
        """
        self.set_object(obj)
