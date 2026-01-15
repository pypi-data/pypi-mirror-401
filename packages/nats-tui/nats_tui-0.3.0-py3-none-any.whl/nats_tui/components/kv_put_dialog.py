"""Dialog for putting/editing a Key/Value entry."""

from dataclasses import dataclass

from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, TextArea


@dataclass
class KVPutResult:
    """Result from put KV value dialog."""

    key: str
    value: str


class KVPutDialog(ModalScreen[KVPutResult | None]):
    """Dialog for putting a new KV value or editing an existing one."""

    BINDINGS = [("escape", "cancel", "Cancel")]

    DEFAULT_CSS = """
    KVPutDialog {
        align: center middle;
    }

    #kv_put_dialog {
        width: 80;
        height: auto;
        max-height: 35;
        border: round $primary;
        background: $surface;
        padding: 1 2;
    }

    #kv_put_title {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }

    #kv_put_dialog .field_label {
        margin-top: 1;
        color: $text-muted;
    }

    #kv_put_dialog Input {
        width: 100%;
        margin-bottom: 0;
    }

    #kv_put_dialog TextArea {
        width: 100%;
        height: 12;
        margin-bottom: 0;
    }

    #kv_put_dialog #button_row {
        height: auto;
        align: center middle;
        margin-top: 2;
    }

    #kv_put_dialog Button {
        margin: 0 2;
    }
    """

    def __init__(
        self,
        bucket: str,
        key: str | None = None,
        value: str | None = None,
        edit_mode: bool = False,
    ) -> None:
        """Initialize the dialog.

        Args:
            bucket: Bucket name (for display)
            key: Pre-filled key name (for edit mode)
            value: Pre-filled value (for edit mode)
            edit_mode: If True, key field is disabled
        """
        super().__init__()
        self._bucket = bucket
        self._key = key or ""
        self._value = value or ""
        self._edit_mode = edit_mode

    def compose(self) -> ComposeResult:
        """Create the dialog widgets."""
        title = f"Edit Key in '{self._bucket}'" if self._edit_mode else f"Put Key in '{self._bucket}'"

        with Container(id="kv_put_dialog"):
            yield Label(title, id="kv_put_title")

            yield Label("Key", classes="field_label")
            yield Input(
                placeholder="my.key.name",
                value=self._key,
                id="key_name",
                disabled=self._edit_mode,
            )

            yield Label("Value", classes="field_label")
            yield TextArea(
                self._value,
                id="value_area",
            )

            with Horizontal(id="button_row"):
                yield Button("Cancel", variant="default", id="cancel_btn")
                yield Button("Save", variant="primary", id="save_btn")

    def on_mount(self) -> None:
        """Focus the appropriate input on mount."""
        if self._edit_mode:
            self.query_one("#value_area", TextArea).focus()
        else:
            self.query_one("#key_name", Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "cancel_btn":
            self.dismiss(None)
        elif event.button.id == "save_btn":
            self._save_value()

    def _save_value(self) -> None:
        """Validate and save the value."""
        key = self.query_one("#key_name", Input).value.strip()
        value = self.query_one("#value_area", TextArea).text

        # Validate key
        if not key:
            self.notify("Key name is required", severity="error")
            return

        # Key validation - dots allowed for hierarchical keys
        if not all(c.isalnum() or c in "-_." for c in key):
            self.notify(
                "Key can only contain letters, numbers, dots, hyphens, and underscores",
                severity="error",
            )
            return

        self.dismiss(KVPutResult(key=key, value=value))

    def action_cancel(self) -> None:
        """Cancel the dialog."""
        self.dismiss(None)
