"""Message detail panel for NATS TUI."""

from textual.reactive import reactive
from textual.widgets import Static

from nats_tui.messages import ReceivedMessage


class MessageDetail(Static):
    """Panel showing full details of the selected message."""

    DEFAULT_CSS = """
    MessageDetail {
        width: 1fr;
        height: 1fr;
        border: round $primary;
        background: $surface;
        padding: 1 2;
        overflow-y: auto;
    }
    """

    message: reactive[ReceivedMessage | None] = reactive(None)

    def render(self) -> str:
        """Render the message details."""
        if not self.message:
            return (
                "No message selected\n\n"
                "Select a message from the list\n"
                "to view its full payload."
            )

        timestamp = self.message.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return (
            f"Subject: {self.message.subject}\n"
            f"Received: {timestamp}\n"
            f"Size: {self.message.size} bytes\n\n"
            f"Payload:\n{self.message.payload_str}"
        )
