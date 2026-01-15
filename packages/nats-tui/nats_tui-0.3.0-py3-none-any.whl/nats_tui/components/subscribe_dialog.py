"""Subscribe dialog for NATS TUI."""

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label


class SubscribeDialog(ModalScreen[str | None]):
    """Modal dialog for subscribing to a NATS subject."""

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
    ]

    def __init__(self, initial_subject: str = "") -> None:
        super().__init__()
        self._initial_subject = initial_subject

    def compose(self) -> ComposeResult:
        with Vertical(id="subscribe_dialog"):
            yield Label("Subscribe to Subject", id="subscribe_title")
            yield Input(
                value=self._initial_subject,
                placeholder="e.g., orders.> or orders.created",
                id="subject_input",
            )
            yield Label(
                "Wildcards: * (single token), > (multi token)",
                id="wildcard_hint",
            )
            with Horizontal(id="button_row"):
                yield Button("Cancel", variant="default", id="cancel")
                yield Button("Subscribe", variant="primary", id="subscribe")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "subscribe":
            self._do_subscribe()
        else:
            self.dismiss(None)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle enter key in input."""
        self._do_subscribe()

    def action_cancel(self) -> None:
        """Cancel and close dialog."""
        self.dismiss(None)

    def _do_subscribe(self) -> None:
        """Validate and submit subscription request."""
        subject_input = self.query_one("#subject_input", Input)
        subject = subject_input.value.strip()

        if not subject:
            self.notify("Subject is required", severity="error")
            subject_input.focus()
            return

        self.dismiss(subject)
