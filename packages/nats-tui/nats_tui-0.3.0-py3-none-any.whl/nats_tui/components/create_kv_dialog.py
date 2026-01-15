"""Dialog for creating a new Key/Value bucket."""

from dataclasses import dataclass

from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Select


@dataclass
class CreateKVResult:
    """Result from create KV bucket dialog."""

    name: str
    history: int
    ttl: float
    max_bytes: int
    storage: str


class CreateKVDialog(ModalScreen[CreateKVResult | None]):
    """Dialog for creating a new KV bucket."""

    BINDINGS = [("escape", "cancel", "Cancel")]

    DEFAULT_CSS = """
    CreateKVDialog {
        align: center middle;
    }

    #create_kv_dialog {
        width: 70;
        height: auto;
        border: round $primary;
        background: $surface;
        padding: 1 2;
    }

    #create_kv_title {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }

    #create_kv_dialog .field_label {
        margin-top: 1;
        color: $text-muted;
    }

    #create_kv_dialog Input {
        width: 100%;
        margin-bottom: 0;
    }

    #create_kv_dialog Select {
        width: 100%;
        margin-bottom: 0;
    }

    #create_kv_dialog #button_row {
        height: auto;
        align: center middle;
        margin-top: 2;
    }

    #create_kv_dialog Button {
        margin: 0 2;
    }
    """

    def compose(self) -> ComposeResult:
        """Create the dialog widgets."""
        with Container(id="create_kv_dialog"):
            yield Label("Create Key/Value Bucket", id="create_kv_title")

            yield Label("Bucket Name", classes="field_label")
            yield Input(placeholder="my-bucket", id="bucket_name")

            yield Label("History Depth (1-64)", classes="field_label")
            yield Input(placeholder="1", value="1", id="history")

            yield Label("TTL (seconds, 0 = no expiry)", classes="field_label")
            yield Input(placeholder="0", value="0", id="ttl")

            yield Label("Max Size (bytes, -1 = unlimited)", classes="field_label")
            yield Input(placeholder="-1", value="-1", id="max_bytes")

            yield Label("Storage Type", classes="field_label")
            yield Select(
                [("File", "file"), ("Memory", "memory")],
                value="file",
                id="storage",
            )

            with Horizontal(id="button_row"):
                yield Button("Cancel", variant="default", id="cancel_btn")
                yield Button("Create", variant="primary", id="create_btn")

    def on_mount(self) -> None:
        """Focus the name input on mount."""
        self.query_one("#bucket_name", Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "cancel_btn":
            self.dismiss(None)
        elif event.button.id == "create_btn":
            self._create_bucket()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle enter key in input fields."""
        self._create_bucket()

    def _create_bucket(self) -> None:
        """Validate and create the bucket."""
        name = self.query_one("#bucket_name", Input).value.strip()

        # Validate name
        if not name:
            self.notify("Bucket name is required", severity="error")
            return

        # Validate name format (alphanumeric, hyphens, underscores)
        if not all(c.isalnum() or c in "-_" for c in name):
            self.notify(
                "Bucket name can only contain letters, numbers, hyphens, and underscores",
                severity="error",
            )
            return

        # Parse history
        history_str = self.query_one("#history", Input).value.strip()
        try:
            history = int(history_str) if history_str else 1
            if history < 1 or history > 64:
                self.notify("History must be between 1 and 64", severity="error")
                return
        except ValueError:
            self.notify("Invalid history value", severity="error")
            return

        # Parse TTL
        ttl_str = self.query_one("#ttl", Input).value.strip()
        try:
            ttl = float(ttl_str) if ttl_str else 0
            if ttl < 0:
                self.notify("TTL cannot be negative", severity="error")
                return
        except ValueError:
            self.notify("Invalid TTL value", severity="error")
            return

        # Parse max bytes
        max_bytes_str = self.query_one("#max_bytes", Input).value.strip()
        try:
            max_bytes = int(max_bytes_str) if max_bytes_str else -1
        except ValueError:
            self.notify("Invalid max bytes value", severity="error")
            return

        # Get storage type
        storage = self.query_one("#storage", Select).value

        self.dismiss(
            CreateKVResult(
                name=name,
                history=history,
                ttl=ttl,
                max_bytes=max_bytes,
                storage=storage,
            )
        )

    def action_cancel(self) -> None:
        """Cancel the dialog."""
        self.dismiss(None)
