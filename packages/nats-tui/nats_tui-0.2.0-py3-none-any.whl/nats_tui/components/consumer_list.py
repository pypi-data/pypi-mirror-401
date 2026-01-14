"""Consumer list widget for JetStream consumers."""

from textual.message import Message
from textual.widgets import Label, ListItem, ListView

from nats_tui.messages import ConsumerInfo


class ConsumerList(ListView):
    """List of JetStream consumers for a stream."""

    class ConsumerSelected(Message):
        """Posted when a consumer is selected."""

        def __init__(self, consumer: ConsumerInfo) -> None:
            super().__init__()
            self.consumer = consumer

    def __init__(self) -> None:
        super().__init__(id="consumer_list")
        self._consumers: list[ConsumerInfo] = []
        self._stream_name: str = ""

    def set_consumers(self, stream_name: str, consumers: list[ConsumerInfo]) -> None:
        """Update the consumer list.

        Args:
            stream_name: Name of the stream these consumers belong to
            consumers: List of ConsumerInfo objects
        """
        self._stream_name = stream_name
        self._consumers = consumers
        self.clear()
        for consumer in consumers:
            # Build label with pause indicator and pending count
            pause_icon = "[P]" if consumer.paused else "   "
            pending = f"{consumer.num_pending:,}" if consumer.num_pending else "0"
            label = f"{pause_icon} {consumer.name} ({pending} pending)"
            item = ListItem(Label(label))
            item._consumer_info = consumer  # type: ignore
            self.append(item)

        # Ensure the first item is selected after loading
        if consumers:
            self.index = 0

    def clear_consumers(self) -> None:
        """Clear all consumers from the list."""
        self._consumers.clear()
        self._stream_name = ""
        self.clear()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle consumer selection (Enter key)."""
        if event.item and hasattr(event.item, "_consumer_info"):
            self.post_message(self.ConsumerSelected(event.item._consumer_info))

    @property
    def selected_consumer(self) -> ConsumerInfo | None:
        """Get the currently selected consumer."""
        if self.index is not None and 0 <= self.index < len(self._consumers):
            return self._consumers[self.index]
        return None

    @property
    def stream_name(self) -> str:
        """Get the stream name for these consumers."""
        return self._stream_name
