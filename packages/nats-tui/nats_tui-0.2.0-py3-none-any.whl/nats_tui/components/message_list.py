"""Message list widget for NATS TUI."""

from textual.message import Message
from textual.widgets import ListItem, ListView, Static

from nats_tui.messages import ReceivedMessage


class MessageList(ListView):
    """Scrollable list of received messages."""

    DEFAULT_CSS = """
    MessageList {
        width: 1fr;
        height: 1fr;
        border: round $primary;
        background: $surface;
    }
    MessageList:focus {
        border: round $secondary;
    }
    """

    class MessageSelected(Message):
        """Posted when a message is selected in the list."""

        def __init__(self, message: ReceivedMessage) -> None:
            super().__init__()
            self.message = message

    def __init__(self) -> None:
        super().__init__(id="message_list")
        self._messages: list[ReceivedMessage] = []
        self._max_messages = 100  # Keep last 100 messages

    def add_message(self, msg: ReceivedMessage) -> None:
        """Add a message to the list (newest first)."""
        self._messages.insert(0, msg)

        # Trim old messages
        if len(self._messages) > self._max_messages:
            self._messages = self._messages[: self._max_messages]
            # Remove oldest list item
            if len(self.children) > self._max_messages:
                self.children[-1].remove()

        # Create list item with message preview
        timestamp = msg.timestamp.strftime("%H:%M:%S")
        content = f"{timestamp} {msg.subject}\n  {msg.preview}"
        item = ListItem(Static(content, classes="message_item"))

        # Store reference to message
        item._received_message = msg  # type: ignore

        # Insert at top
        self.insert(0, [item])

    def clear_messages(self) -> None:
        """Clear all messages from the list."""
        self._messages.clear()
        self.clear()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle message selection."""
        if hasattr(event.item, "_received_message"):
            self.post_message(self.MessageSelected(message=event.item._received_message))

    @property
    def message_count(self) -> int:
        """Get the number of messages in the list."""
        return len(self._messages)
