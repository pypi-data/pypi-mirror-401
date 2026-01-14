"""Stream message list widget for browsing JetStream messages."""

from textual.message import Message
from textual.widgets import ListItem, ListView, Static

from nats_tui.messages import StreamMessageInfo


class StreamMessageList(ListView):
    """Scrollable list of messages from a JetStream stream."""

    DEFAULT_CSS = """
    StreamMessageList {
        width: 1fr;
        height: 1fr;
        border: round $primary;
        background: $surface;
    }
    StreamMessageList:focus {
        border: round $secondary;
    }
    StreamMessageList > ListItem {
        padding: 0 1;
    }
    """

    class MessageSelected(Message):
        """Posted when a message is selected in the list."""

        def __init__(self, message: StreamMessageInfo) -> None:
            super().__init__()
            self.message = message

    def __init__(self) -> None:
        super().__init__(id="stream_message_list")
        self._messages: list[StreamMessageInfo] = []
        self._stream_name: str = ""
        # Pagination state
        self._first_seq: int = 0
        self._last_seq: int = 0
        self._total_count: int = 0
        self._page_start_seq: int | None = None

    def set_messages(
        self,
        stream_name: str,
        messages: list[StreamMessageInfo],
        first_seq: int = 0,
        last_seq: int = 0,
        total_count: int = 0,
        page_start_seq: int | None = None,
    ) -> None:
        """Set the list of messages to display with pagination info.

        Args:
            stream_name: Name of the stream
            messages: List of StreamMessageInfo objects
            first_seq: Stream's first sequence number
            last_seq: Stream's last sequence number
            total_count: Total messages in stream
            page_start_seq: Starting sequence of current page
        """
        self._stream_name = stream_name
        self._messages = messages
        self._first_seq = first_seq
        self._last_seq = last_seq
        self._total_count = total_count
        self._page_start_seq = page_start_seq
        self.clear()

        # Update border title with pagination info
        self._update_border_title()

        if not messages:
            item = ListItem(Static("No messages in stream"))
            self.append(item)
            return

        for msg in messages:
            # Format: seq | time | subject (single line to avoid rendering issues)
            time_str = msg.time.strftime("%H:%M:%S") if msg.time else "??:??:??"
            # Truncate preview to keep display simple
            preview = msg.preview[:30] + "..." if len(msg.preview) > 30 else msg.preview
            content = f"#{msg.seq} {time_str} {msg.subject} - {preview}"
            item = ListItem(Static(content))
            # Store reference to message
            item._stream_message = msg  # type: ignore
            self.append(item)

        # Ensure the first item is selected after loading
        if messages:
            self.index = 0

    def _update_border_title(self) -> None:
        """Update border title with pagination info."""
        if self._total_count == 0:
            self.border_title = "Messages (empty)"
            return

        if self._messages:
            # Show range of sequences displayed
            if len(self._messages) > 0:
                displayed_seqs = [m.seq for m in self._messages]
                min_seq = min(displayed_seqs)
                max_seq = max(displayed_seqs)
                self.border_title = (
                    f"Messages #{min_seq}-{max_seq} of {self._total_count} "
                    f"(n=older, p=newer)"
                )
            else:
                self.border_title = f"Messages (0 of {self._total_count})"
        else:
            self.border_title = "Messages"

    def clear_messages(self) -> None:
        """Clear all messages from the list."""
        self._messages.clear()
        self._stream_name = ""
        self.clear()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle message selection (Enter key)."""
        if hasattr(event.item, "_stream_message"):
            self.post_message(self.MessageSelected(message=event.item._stream_message))

    @property
    def selected_message(self) -> StreamMessageInfo | None:
        """Get the currently highlighted message."""
        if self.index is not None and 0 <= self.index < len(self._messages):
            return self._messages[self.index]
        return None

    @property
    def stream_name(self) -> str:
        """Get the current stream name."""
        return self._stream_name

    @property
    def message_count(self) -> int:
        """Get the number of messages in the list."""
        return len(self._messages)
