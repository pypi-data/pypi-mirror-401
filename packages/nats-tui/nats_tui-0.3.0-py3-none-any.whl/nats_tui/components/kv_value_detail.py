"""Key/Value value detail widget for displaying key-value information."""

from textual.reactive import reactive
from textual.widgets import Static

from nats_tui.messages import KVEntry


def _format_bytes(num_bytes: int) -> str:
    """Format bytes into human-readable string."""
    if num_bytes < 0:
        return "unlimited"
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} PB"


class KVValueDetail(Static):
    """Display key-value details."""

    entry: reactive[KVEntry | None] = reactive(None)

    def render(self) -> str:
        """Render key-value details."""
        if not self.entry:
            return (
                "Select a key to view its value...\n\n"
                "[dim]Key/Value Actions[/dim]\n"
                "  n = New key\n"
                "  e = Edit value\n"
                "  Delete = Delete key\n"
                "  r = Refresh\n"
                "  Escape = Back to subjects\n"
                "  ? = Help"
            )

        e = self.entry

        # Format timestamp
        created_str = "Unknown"
        if e.created:
            created_str = e.created.strftime("%Y-%m-%d %H:%M:%S UTC")

        # Format value - show full value or truncate if too long
        value_display = e.value_str
        if len(value_display) > 500:
            value_display = value_display[:500] + "\n... [truncated]"

        # Operation indicator
        op_indicator = ""
        if e.operation == "DEL":
            op_indicator = " [red](DELETED)[/red]"
        elif e.operation == "PURGE":
            op_indicator = " [yellow](PURGED)[/yellow]"

        return (
            f"[bold]{e.key}[/bold]{op_indicator}\n\n"
            f"[dim]Metadata[/dim]\n"
            f"  Bucket: {e.bucket}\n"
            f"  Revision: {e.revision}\n"
            f"  Size: {_format_bytes(e.size)}\n"
            f"  Created: {created_str}\n"
            f"  Operation: {e.operation}\n\n"
            f"[dim]Value[/dim]\n"
            f"{value_display}\n\n"
            f"[dim]Actions[/dim]  n=New  e=Edit  Delete=Delete  r=Refresh"
        )
