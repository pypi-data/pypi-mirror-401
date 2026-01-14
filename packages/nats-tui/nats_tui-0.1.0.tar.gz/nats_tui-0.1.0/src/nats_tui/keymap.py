"""Customizable key bindings for NATS TUI."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class KeyBinding:
    """A key binding mapping keys to an action."""

    keys: str
    action: str
    description: str = ""


# Default key bindings - action name to default key
DEFAULT_KEYBINDINGS: dict[str, str] = {
    # Global actions
    "quit": "q",
    "help": "f1",
    "connect": "c",
    "disconnect": "d",
    "refresh": "r",
    # Navigation
    "go_back": "escape",
    "view_consumers": "enter",
    # View switching
    "show_subjects": "1",
    "show_messages": "2",
    "show_streams": "3",
    # Actions
    "new_item": "n",
    "delete_item": "delete",
    "publish": "p",
    "subscribe": "s",
    "toggle_pause": "space",
    "purge_stream": "ctrl+p",
}

# Action descriptions for help/documentation
ACTION_DESCRIPTIONS: dict[str, str] = {
    "quit": "Quit the application",
    "help": "Show help",
    "connect": "Open connection dialog",
    "disconnect": "Disconnect from server",
    "refresh": "Refresh current view",
    "go_back": "Go back to previous view",
    "view_consumers": "View consumers for selected stream",
    "show_subjects": "Switch to subject browser",
    "show_messages": "Switch to message viewer",
    "show_streams": "Switch to JetStream streams",
    "new_item": "Create new item (stream/consumer)",
    "delete_item": "Delete selected item",
    "publish": "Open publish dialog",
    "subscribe": "Subscribe to subject",
    "toggle_pause": "Pause/resume consumer",
    "purge_stream": "Purge selected stream",
}


@dataclass
class NatsTuiKeyMap:
    """Key map with customized bindings."""

    bindings: dict[str, str]

    @classmethod
    def from_config(cls, custom_bindings: dict[str, str] | None = None) -> "NatsTuiKeyMap":
        """Create a keymap from config, merging with defaults.

        Args:
            custom_bindings: Custom key bindings from config (action -> keys)

        Returns:
            NatsTuiKeyMap with merged bindings
        """
        bindings = DEFAULT_KEYBINDINGS.copy()
        if custom_bindings:
            bindings.update(custom_bindings)
        return cls(bindings=bindings)

    def get_key(self, action: str) -> str:
        """Get the key(s) for an action.

        Args:
            action: Action name

        Returns:
            Key binding string
        """
        return self.bindings.get(action, DEFAULT_KEYBINDINGS.get(action, ""))

    def get_binding(self, action: str) -> KeyBinding:
        """Get full binding info for an action.

        Args:
            action: Action name

        Returns:
            KeyBinding with keys and description
        """
        return KeyBinding(
            keys=self.get_key(action),
            action=action,
            description=ACTION_DESCRIPTIONS.get(action, ""),
        )

    def get_all_bindings(self) -> list[KeyBinding]:
        """Get all key bindings.

        Returns:
            List of all KeyBinding objects
        """
        return [self.get_binding(action) for action in self.bindings]

    def to_textual_bindings(self) -> list[tuple[str, str, str]]:
        """Convert to Textual BINDINGS format.

        Returns:
            List of (key, action, description) tuples
        """
        return [
            (keys, action, ACTION_DESCRIPTIONS.get(action, action))
            for action, keys in self.bindings.items()
        ]
