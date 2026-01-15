"""Stream message detail widget for displaying full message content."""

import json

from textual.reactive import reactive
from textual.widgets import Static

from nats_tui.messages import StreamMessageInfo


def _format_bytes(num_bytes: int) -> str:
    """Format bytes into human-readable string."""
    if num_bytes < 0:
        return "unknown"
    for unit in ["B", "KB", "MB", "GB"]:
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} TB"


def _try_format_json(data: str) -> str:
    """Try to pretty-print JSON data."""
    try:
        parsed = json.loads(data)
        return json.dumps(parsed, indent=2)
    except (json.JSONDecodeError, TypeError):
        return data


class StreamMessageDetail(Static):
    """Display full stream message details."""

    DEFAULT_CSS = """
    StreamMessageDetail {
        width: 1fr;
        height: 1fr;
        border: round $primary;
        background: $surface;
        padding: 1;
        overflow-y: auto;
    }
    """

    message: reactive[StreamMessageInfo | None] = reactive(None)

    def render(self) -> str:
        """Render message details."""
        if not self.message:
            return (
                "Select a message to view details...\n\n"
                "[dim]Navigation:[/dim]\n"
                "  j: Return to stream list\n"
                "  Escape: Go back to stream list\n\n"
                "[dim]Actions:[/dim]\n"
                "  P: Purge all messages from stream"
            )

        msg = self.message

        # Format timestamp
        time_str = msg.time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] if msg.time else "unknown"

        # Format headers
        headers_str = ""
        if msg.headers:
            headers_lines = [f"    {k}: {v}" for k, v in msg.headers.items()]
            headers_str = "\n".join(headers_lines)
        else:
            headers_str = "    (none)"

        # Format data - try to pretty-print JSON
        data_str = msg.data_str
        if data_str.startswith("{") or data_str.startswith("["):
            data_str = _try_format_json(data_str)

        return (
            f"[bold]Message #{msg.seq}[/bold]\n\n"
            f"[dim]Metadata[/dim]\n"
            f"  Subject: {msg.subject}\n"
            f"  Sequence: {msg.seq}\n"
            f"  Time: {time_str}\n"
            f"  Size: {_format_bytes(msg.size)}\n\n"
            f"[dim]Headers[/dim]\n"
            f"{headers_str}\n\n"
            f"[dim]Data[/dim]\n"
            f"{data_str}\n\n"
            f"[dim]Actions[/dim]\n"
            f"  Delete: Delete this message\n"
            f"  P: Purge all messages from stream\n"
            f"  j: Return to stream list"
        )
