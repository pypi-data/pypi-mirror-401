"""Stream list widget for JetStream streams."""

from textual.message import Message
from textual.widgets import Label, ListItem, ListView

from nats_tui.messages import StreamInfo


class StreamList(ListView):
    """List of JetStream streams."""

    class StreamSelected(Message):
        """Posted when a stream is selected."""

        def __init__(self, stream: StreamInfo) -> None:
            super().__init__()
            self.stream = stream

    def __init__(self) -> None:
        super().__init__(id="stream_list")
        self._streams: list[StreamInfo] = []

    def set_streams(self, streams: list[StreamInfo]) -> None:
        """Update the stream list.

        Args:
            streams: List of StreamInfo objects
        """
        self._streams = streams
        self.clear()
        for stream in streams:
            storage_icon = "F" if stream.storage == "file" else "M"
            label = f"[{storage_icon}] {stream.name} ({stream.messages:,} msgs)"
            item = ListItem(Label(label))
            item._stream_info = stream  # type: ignore
            self.append(item)

        # Ensure the first item is selected after loading
        if streams:
            self.index = 0

    def clear_streams(self) -> None:
        """Clear all streams from the list."""
        self._streams.clear()
        self.clear()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle stream selection (Enter key)."""
        if event.item and hasattr(event.item, "_stream_info"):
            self.post_message(self.StreamSelected(event.item._stream_info))

    @property
    def selected_stream(self) -> StreamInfo | None:
        """Get the currently selected stream."""
        if self.index is not None and 0 <= self.index < len(self._streams):
            return self._streams[self.index]
        return None
