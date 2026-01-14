"""Stream detail widget for displaying stream information."""

from textual.reactive import reactive
from textual.widgets import Static

from nats_tui.messages import StreamInfo


def _format_bytes(num_bytes: int) -> str:
    """Format bytes into human-readable string."""
    if num_bytes < 0:
        return "unlimited"
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} PB"


def _format_age(seconds: float) -> str:
    """Format age in seconds to human-readable string."""
    if seconds <= 0:
        return "unlimited"
    if seconds < 60:
        return f"{seconds:.0f} seconds"
    if seconds < 3600:
        return f"{seconds / 60:.1f} minutes"
    if seconds < 86400:
        return f"{seconds / 3600:.1f} hours"
    return f"{seconds / 86400:.1f} days"


class StreamDetail(Static):
    """Display stream details."""

    stream: reactive[StreamInfo | None] = reactive(None)

    def render(self) -> str:
        """Render stream details."""
        if not self.stream:
            return "Select a stream to view details...\n\nPress 'n' to create a new stream."

        s = self.stream

        # Format subjects (show first 3, then count)
        subjects = ", ".join(s.subjects[:3])
        if len(s.subjects) > 3:
            subjects += f" (+{len(s.subjects) - 3} more)"

        # Format limits
        max_msgs = f"{s.max_msgs:,}" if s.max_msgs > 0 else "unlimited"
        max_bytes = _format_bytes(s.max_bytes)
        max_age = _format_age(s.max_age)

        return (
            f"[bold]{s.name}[/bold]\n\n"
            f"[dim]Configuration[/dim]\n"
            f"  Subjects: {subjects}\n"
            f"  Storage: {s.storage}\n"
            f"  Retention: {s.retention}\n"
            f"  Max Messages: {max_msgs}\n"
            f"  Max Bytes: {max_bytes}\n"
            f"  Max Age: {max_age}\n\n"
            f"[dim]State[/dim]\n"
            f"  Messages: {s.messages:,}\n"
            f"  Bytes: {_format_bytes(s.bytes)}\n"
            f"  First Seq: {s.first_seq}\n"
            f"  Last Seq: {s.last_seq}\n"
            f"  Consumers: {s.consumers}\n\n"
            f"[dim]Actions[/dim]\n"
            f"  View Messages: press 'm' key\n"
            f"  View Consumers: press 'Enter' key\n"
            f"  Delete: press 'Delete' key\n"
            f"  Purge: press 'P' key"
        )
