"""Publish dialog for NATS TUI."""

from dataclasses import dataclass

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, TextArea


@dataclass
class PublishResult:
    """Result from publish dialog."""

    subject: str
    payload: bytes
    headers: dict[str, str] | None = None


class PublishDialog(ModalScreen[PublishResult | None]):
    """Modal dialog for publishing messages to NATS."""

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
    ]

    def __init__(self, initial_subject: str = "") -> None:
        super().__init__()
        self._initial_subject = initial_subject

    def compose(self) -> ComposeResult:
        with Vertical(id="publish_dialog"):
            yield Label("Publish Message", id="publish_title")
            yield Label("Subject:")
            yield Input(
                value=self._initial_subject,
                placeholder="e.g., orders.created",
                id="subject_input",
            )
            yield Label("Payload:")
            yield TextArea(id="payload_input")
            yield Label("Headers (optional, key:value per line):")
            yield TextArea(id="headers_input", classes="headers_area")
            with Horizontal(id="button_row"):
                yield Button("Cancel", variant="default", id="cancel")
                yield Button("Publish", variant="primary", id="publish")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "publish":
            self._do_publish()
        else:
            self.dismiss(None)

    def action_cancel(self) -> None:
        """Cancel and close dialog."""
        self.dismiss(None)

    def _do_publish(self) -> None:
        """Validate and submit publish request."""
        subject_input = self.query_one("#subject_input", Input)
        payload_input = self.query_one("#payload_input", TextArea)
        headers_input = self.query_one("#headers_input", TextArea)

        subject = subject_input.value.strip()
        if not subject:
            self.notify("Subject is required", severity="error")
            subject_input.focus()
            return

        payload = payload_input.text
        headers = self._parse_headers(headers_input.text)

        self.dismiss(
            PublishResult(
                subject=subject,
                payload=payload.encode(),
                headers=headers,
            )
        )

    def _parse_headers(self, text: str) -> dict[str, str] | None:
        """Parse headers from text input.

        Format: key:value per line
        """
        if not text.strip():
            return None

        headers = {}
        for line in text.strip().split("\n"):
            line = line.strip()
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                if key:
                    headers[key] = value

        return headers if headers else None
