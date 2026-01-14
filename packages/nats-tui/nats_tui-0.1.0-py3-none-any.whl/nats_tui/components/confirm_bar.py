"""Inline confirmation bar widget - alternative to modal dialogs."""

import logging
from dataclasses import dataclass

from textual import events
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Button, Label

logger = logging.getLogger(__name__)


class ConfirmBar(Widget):
    """Inline confirmation bar that appears at the bottom of a view.

    Shows a message with Yes/No buttons. Emits Confirmed or Cancelled message.
    """

    DEFAULT_CSS = """
    ConfirmBar {
        dock: bottom;
        height: auto;
        background: $error-darken-2;
        padding: 0 1;
        display: none;
    }

    ConfirmBar.visible {
        display: block;
    }

    ConfirmBar Horizontal {
        height: auto;
        align: center middle;
    }

    ConfirmBar Label {
        margin: 0 1;
        text-style: bold;
    }

    ConfirmBar Button {
        margin: 0 1;
        min-width: 8;
    }

    ConfirmBar #yes_btn {
        background: $error;
    }
    """

    @dataclass
    class Confirmed(Message):
        """Posted when user confirms the action."""
        action: str
        context: dict

    @dataclass
    class Cancelled(Message):
        """Posted when user cancels the action."""
        action: str

    def __init__(self) -> None:
        super().__init__()
        self._action: str = ""
        self._context: dict = {}

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label("", id="confirm_message")
            yield Button("Yes", id="yes_btn", variant="error")
            yield Button("No", id="no_btn", variant="default")

    def show(self, message: str, action: str, context: dict | None = None) -> None:
        """Show the confirmation bar with the given message."""
        logger.debug(f"ConfirmBar.show: {message}")
        self._action = action
        self._context = context or {}
        self.query_one("#confirm_message", Label).update(message)
        self.add_class("visible")
        # Focus the Yes button
        self.query_one("#yes_btn", Button).focus()

    def hide(self) -> None:
        """Hide the confirmation bar."""
        logger.debug("ConfirmBar.hide")
        self.remove_class("visible")
        self._action = ""
        self._context = {}

    @property
    def is_visible(self) -> bool:
        """Check if the bar is currently visible."""
        return self.has_class("visible")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks."""
        event.stop()
        if event.button.id == "yes_btn":
            logger.debug(f"ConfirmBar: confirmed action={self._action}")
            self.post_message(self.Confirmed(action=self._action, context=self._context))
        else:
            logger.debug(f"ConfirmBar: cancelled action={self._action}")
            self.post_message(self.Cancelled(action=self._action))
        self.hide()

    def on_key(self, event: events.Key) -> None:
        """Handle key events when bar is visible."""
        if not self.is_visible:
            return

        if event.key == "escape":
            event.stop()
            logger.debug("ConfirmBar: escape pressed")
            self.post_message(self.Cancelled(action=self._action))
            self.hide()
        elif event.key == "y":
            event.stop()
            logger.debug("ConfirmBar: 'y' pressed - confirming")
            self.post_message(self.Confirmed(action=self._action, context=self._context))
            self.hide()
        elif event.key == "n":
            event.stop()
            logger.debug("ConfirmBar: 'n' pressed - cancelling")
            self.post_message(self.Cancelled(action=self._action))
            self.hide()
