"""Dialog for creating a new JetStream consumer."""

from dataclasses import dataclass

from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Select


@dataclass
class CreateConsumerResult:
    """Result from create consumer dialog."""

    name: str
    durable_name: str | None
    deliver_policy: str
    ack_policy: str
    filter_subject: str | None


class CreateConsumerDialog(ModalScreen[CreateConsumerResult | None]):
    """Dialog for creating a new consumer."""

    BINDINGS = [("escape", "cancel", "Cancel")]

    def __init__(self, stream_name: str) -> None:
        super().__init__()
        self._stream_name = stream_name

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        with Container(id="create_consumer_dialog"):
            yield Label(f"Create Consumer for '{self._stream_name}'", id="create_consumer_title")
            yield Label("Consumer Name:", classes="field_label")
            yield Input(placeholder="my-consumer", id="consumer_name")
            yield Label("Deliver Policy:", classes="field_label")
            yield Select(
                [
                    ("All (replay all messages)", "all"),
                    ("New (only new messages)", "new"),
                    ("Last (latest message only)", "last"),
                ],
                value="all",
                id="deliver_policy",
            )
            yield Label("Ack Policy:", classes="field_label")
            yield Select(
                [
                    ("Explicit (require manual ack)", "explicit"),
                    ("None (no ack required)", "none"),
                    ("All (ack all previous)", "all"),
                ],
                value="explicit",
                id="ack_policy",
            )
            yield Label("Filter Subject (optional):", classes="field_label")
            yield Input(placeholder="events.> or leave empty for all", id="filter_subject")
            with Horizontal(id="button_row"):
                yield Button("Cancel", variant="default", id="cancel_btn")
                yield Button("Create", variant="primary", id="create_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "cancel_btn":
            self.dismiss(None)
        elif event.button.id == "create_btn":
            self._create_consumer()

    def _create_consumer(self) -> None:
        """Validate and create consumer."""
        name = self.query_one("#consumer_name", Input).value.strip()
        deliver_policy = self.query_one("#deliver_policy", Select).value
        ack_policy = self.query_one("#ack_policy", Select).value
        filter_subject = self.query_one("#filter_subject", Input).value.strip()

        # Validate
        if not name:
            self.notify("Consumer name is required", severity="error")
            return

        self.dismiss(
            CreateConsumerResult(
                name=name,
                durable_name=name,  # Use same name for durable
                deliver_policy=str(deliver_policy),
                ack_policy=str(ack_policy),
                filter_subject=filter_subject if filter_subject else None,
            )
        )

    def action_cancel(self) -> None:
        """Cancel the dialog."""
        self.dismiss(None)
