"""Base App class for NATS TUI with theme registration."""

from typing import Union

from textual.app import App
from textual.driver import Driver

from nats_tui.colors import (
    DEFAULT_THEME,
    NATS_TUI_LIGHT_THEME,
    NATS_TUI_TEXTUAL_THEME,
    OSCAR_LIGHT_THEME,
    OSCAR_THEME,
    VALID_THEMES,
)
from nats_tui.exception import NatsTuiThemeError, pretty_error_message


class AppBase(App, inherit_bindings=False):
    """A common base app for NATS TUI and its mini-apps."""

    def __init__(
        self,
        *,
        theme: str | None = None,
        driver_class: Union[type[Driver], None] = None,
        css_path: Union[str, list[str], None] = None,
        watch_css: bool = False,
    ) -> None:
        super().__init__(driver_class=driver_class, css_path=css_path, watch_css=watch_css)
        # Register custom themes
        self.register_theme(OSCAR_THEME)
        self.register_theme(OSCAR_LIGHT_THEME)
        self.register_theme(NATS_TUI_TEXTUAL_THEME)
        self.register_theme(NATS_TUI_LIGHT_THEME)
        try:
            self.theme = theme or DEFAULT_THEME
        except Exception:
            valid_themes = ", ".join(VALID_THEMES.keys())
            e = NatsTuiThemeError(
                f"No theme found with the name {theme}.\n"
                f"Supported themes: {valid_themes}",
                title="NATS TUI couldn't load your theme.",
            )
            self.exit(return_code=2, message=pretty_error_message(e))
