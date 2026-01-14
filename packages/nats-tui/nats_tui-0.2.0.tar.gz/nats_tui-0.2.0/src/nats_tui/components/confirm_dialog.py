"""Confirmation dialog for destructive actions.

Simplified to match Harlequin's ConfirmModal pattern - no BINDINGS, just button handlers.
"""

import logging
from dataclasses import dataclass

from textual import events
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label

logger = logging.getLogger(__name__)


@dataclass
class ConfirmResult:
    """Result from confirmation dialog."""

    confirmed: bool
    action: str  # The action identifier
    context: dict  # Additional context data


class ConfirmDialog(ModalScreen[bool]):
    """Simple confirmation modal (Harlequin-style).

    Returns True if confirmed, False if cancelled.
    """

    DEFAULT_CSS = """
    ConfirmDialog {
        align: center middle;
    }

    ConfirmDialog > Vertical {
        width: auto;
        height: auto;
        max-width: 80;
        border: thick $error;
        background: $surface;
        padding: 1 2;
    }

    ConfirmDialog Label {
        width: 100%;
        text-align: center;
        margin: 1 0;
    }

    ConfirmDialog #title_label {
        text-style: bold;
        color: $error;
    }

    ConfirmDialog #warning_label {
        color: $warning;
        text-style: italic;
    }

    ConfirmDialog Horizontal {
        width: auto;
        height: auto;
        align: center middle;
        margin-top: 1;
    }

    ConfirmDialog Button {
        margin: 0 2;
    }
    """

    def __init__(
        self,
        title: str,
        message: str,
        action: str = "",
        context: dict | None = None,
        details: str | None = None,
        warning: str | None = None,
        confirm_label: str = "Yes",
        cancel_label: str = "No",
    ) -> None:
        logger.debug(f"ConfirmDialog.__init__: title={title}")
        super().__init__()
        self._title = title
        self._message = message
        self._action = action
        self._context = context or {}
        self._details = details
        self._warning = warning
        self._confirm_label = confirm_label
        self._cancel_label = cancel_label
        logger.debug("ConfirmDialog.__init__ done")

    def compose(self) -> ComposeResult:
        logger.debug("ConfirmDialog.compose() START")
        with Vertical():
            yield Label(self._title, id="title_label")
            yield Label(self._message, id="message_label")
            if self._details:
                yield Label(self._details, id="details_label")
            if self._warning:
                yield Label(self._warning, id="warning_label")
            with Horizontal():
                yield Button(self._cancel_label, id="no_btn")
                yield Button(self._confirm_label, variant="error", id="yes_btn")
        logger.debug("ConfirmDialog.compose() END")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        logger.debug(f"ConfirmDialog button pressed: {event.button.id}")
        event.stop()
        if event.button.id == "yes_btn":
            self.dismiss(True)
        else:
            self.dismiss(False)

    def on_key(self, event: events.Key) -> None:
        """Handle key events like Harlequin."""
        logger.debug(f"ConfirmDialog on_key: {event.key}")
        event.stop()
        if event.key == "escape":
            self.dismiss(False)
        elif event.key == "enter":
            self.dismiss(True)
