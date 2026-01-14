"""Status bar component for displaying connection state."""

from textual.reactive import reactive
from textual.widgets import Static


class StatusBar(Static):
    """Displays NATS connection status."""

    DEFAULT_CSS = """
    StatusBar {
        dock: top;
        height: 1;
        background: $panel;
        color: $text;
        padding: 0 1;
    }
    StatusBar.connected {
        background: $success;
        color: $background;
    }
    StatusBar.connecting {
        background: $warning;
        color: $background;
    }
    StatusBar.disconnected {
        background: $panel;
    }
    """

    status_text: reactive[str] = reactive("Disconnected")
    _state: reactive[str] = reactive("disconnected")

    def render(self) -> str:
        """Render the status bar text."""
        return f"Status: {self.status_text}"

    def watch__state(self, state: str) -> None:
        """Update CSS classes when state changes."""
        self.remove_class("connected", "connecting", "disconnected")
        self.add_class(state)

    def set_connected(self, server_url: str) -> None:
        """Set status to connected."""
        self.status_text = f"Connected to {server_url}"
        self._state = "connected"

    def set_disconnected(self) -> None:
        """Set status to disconnected."""
        self.status_text = "Disconnected"
        self._state = "disconnected"

    def set_connecting(self, server_url: str) -> None:
        """Set status to connecting."""
        self.status_text = f"Connecting to {server_url}..."
        self._state = "connecting"
