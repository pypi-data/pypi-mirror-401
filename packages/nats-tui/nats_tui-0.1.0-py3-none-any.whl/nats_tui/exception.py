"""Custom exception classes for NATS TUI."""

from rich.panel import Panel


class NatsTuiError(Exception):
    """Base exception class with title and message."""

    def __init__(self, msg: str, title: str = "") -> None:
        super().__init__(msg)
        self.msg = msg
        self.title = title


class NatsTuiConfigError(NatsTuiError):
    """Configuration errors."""

    pass


class NatsTuiThemeError(NatsTuiError):
    """Theme loading errors."""

    pass


class NatsTuiConnectionError(NatsTuiError):
    """Connection errors."""

    pass


def pretty_error_message(error: NatsTuiError) -> Panel:
    """Format error as a styled Panel."""
    return Panel.fit(
        str(error),
        title=error.title if error.title else "NATS TUI encountered an error.",
        title_align="left",
        border_style="red",
    )
