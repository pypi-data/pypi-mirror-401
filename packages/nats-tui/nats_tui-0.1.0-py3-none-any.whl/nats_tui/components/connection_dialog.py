"""Connection dialog modal for NATS TUI."""

from dataclasses import dataclass

from textual import work
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Checkbox, Input, Label, Static

from nats_tui.adapter import ConnectionConfig, NatsAdapter
from nats_tui.config import ConnectionProfile, NatsTuiConfig, save_config


@dataclass
class ConnectionResult:
    """Result from connection dialog."""

    server_url: str
    username: str | None
    password: str | None
    # TLS settings
    tls_enabled: bool = False
    tls_ca_cert: str | None = None
    tls_cert: str | None = None
    tls_key: str | None = None
    tls_insecure: bool = False
    # Profile saving
    save_profile: bool = False
    profile_name: str | None = None


class ConnectionDialog(ModalScreen[ConnectionResult | None]):
    """Modal dialog for configuring NATS connection."""

    BINDINGS = [("escape", "cancel", "Cancel")]

    DEFAULT_CSS = """
    ConnectionDialog {
        align: center middle;
    }

    #dialog_outer {
        width: 80;
        height: auto;
        max-height: 95%;
        border: thick $primary;
        background: $surface;
        padding: 1 2;
    }

    #dialog_header {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }

    #dialog_inner {
        height: 1fr;
        min-height: 20;
        max-height: 100%;
    }

    #dialog_inner Label {
        margin-top: 1;
    }

    #dialog_inner Input {
        margin-bottom: 0;
    }

    #tls_section {
        margin-top: 1;
        padding: 1;
        border: round $primary-darken-2;
    }

    #tls_section_header {
        text-style: bold;
        color: $text;
        margin-bottom: 0;
    }

    #tls_options {
        height: auto;
    }

    #tls_options.hidden {
        display: none;
    }

    .tls_row {
        height: auto;
        margin-top: 0;
    }

    .tls_row Checkbox {
        width: auto;
        margin-right: 2;
    }

    #save_row {
        margin-top: 1;
        height: auto;
    }

    #save_row Checkbox {
        margin-right: 1;
    }

    #save_row Input {
        width: 1fr;
    }

    #test_result {
        margin-top: 1;
        text-align: center;
        height: auto;
        min-height: 1;
    }

    #test_result.success {
        color: $success;
    }

    #test_result.error {
        color: $error;
    }

    #dialog_buttons {
        margin-top: 2;
        align: center middle;
        height: 3;
    }

    #dialog_buttons Button {
        margin: 0 1;
    }
    """

    def __init__(
        self,
        config: NatsTuiConfig | None = None,
        profile: ConnectionProfile | None = None,
        profile_name: str | None = None,
        tls_config: dict | None = None,
    ) -> None:
        super().__init__()
        self._config = config or NatsTuiConfig()
        self._initial_profile = profile
        self._initial_profile_name = profile_name
        self._tls_config = tls_config or {}

    def compose(self) -> ComposeResult:
        """Create the dialog widgets."""
        # Default values from CLI/tls_config if provided
        server_url = "nats://localhost:4222"
        username = self._tls_config.get("username", "") or ""
        password = self._tls_config.get("password", "") or ""
        profile_name = ""
        tls_enabled = self._tls_config.get("tls_enabled", False)
        tls_ca_cert = self._tls_config.get("tls_ca_cert", "") or ""
        tls_cert = self._tls_config.get("tls_cert", "") or ""
        tls_key = self._tls_config.get("tls_key", "") or ""
        tls_insecure = self._tls_config.get("tls_insecure", False)

        if self._initial_profile:
            server_url = self._initial_profile.get("server", server_url)
            # Only use profile credentials if CLI didn't provide them
            if not username:
                username = self._initial_profile.get("username", "") or ""
            if not password:
                password = self._initial_profile.get("password", "") or ""
            # TLS from profile
            if self._initial_profile.get("tls"):
                tls_enabled = True
            if self._initial_profile.get("tls_ca_cert"):
                tls_ca_cert = self._initial_profile.get("tls_ca_cert", "")
            if self._initial_profile.get("tls_cert"):
                tls_cert = self._initial_profile.get("tls_cert", "")
            if self._initial_profile.get("tls_key"):
                tls_key = self._initial_profile.get("tls_key", "")
            if self._initial_profile.get("tls_insecure"):
                tls_insecure = True
        if self._initial_profile_name:
            profile_name = self._initial_profile_name

        with Vertical(id="dialog_outer"):
            yield Static("Connect to NATS", id="dialog_header")
            with VerticalScroll(id="dialog_inner"):
                yield Label("Server URL:")
                yield Input(
                    value=server_url,
                    placeholder="nats://localhost:4222 or tls://localhost:4222",
                    id="server_url",
                )
                yield Label("Username (optional):")
                yield Input(
                    value=username,
                    id="username",
                    placeholder="Leave empty for no auth",
                )
                yield Label("Password (optional):")
                yield Input(value=password, id="password", password=True)

                # TLS Section
                with Vertical(id="tls_section"):
                    yield Static("TLS Settings", id="tls_section_header")
                    with Horizontal(classes="tls_row"):
                        yield Checkbox(
                            "Enable TLS",
                            value=tls_enabled,
                            id="tls_enabled",
                        )
                        yield Checkbox(
                            "Skip verification (insecure)",
                            value=tls_insecure,
                            id="tls_insecure",
                        )
                    with Vertical(
                        id="tls_options",
                        classes="" if tls_enabled else "hidden",
                    ):
                        yield Label("CA Certificate (optional):")
                        yield Input(
                            value=tls_ca_cert or "",
                            placeholder="/path/to/ca.crt",
                            id="tls_ca_cert",
                        )
                        yield Label("Client Certificate (for mTLS):")
                        yield Input(
                            value=tls_cert or "",
                            placeholder="/path/to/client.crt",
                            id="tls_cert",
                        )
                        yield Label("Client Key (for mTLS):")
                        yield Input(
                            value=tls_key or "",
                            placeholder="/path/to/client.key",
                            id="tls_key",
                        )

                with Horizontal(id="save_row"):
                    yield Checkbox("Save as profile:", id="save_profile")
                    yield Input(
                        value=profile_name,
                        placeholder="profile-name",
                        id="profile_name",
                        disabled=True,
                    )
                yield Static("", id="test_result")
            with Horizontal(id="dialog_buttons"):
                yield Button("Test", variant="default", id="test")
                yield Button("Connect", variant="primary", id="connect")
                yield Button("Cancel", variant="error", id="cancel")

    def on_mount(self) -> None:
        """Focus the server URL input on mount."""
        self.query_one("#server_url", Input).focus()

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        """Handle checkbox changes."""
        if event.checkbox.id == "save_profile":
            profile_input = self.query_one("#profile_name", Input)
            profile_input.disabled = not event.value
        elif event.checkbox.id == "tls_enabled":
            tls_options = self.query_one("#tls_options")
            if event.value:
                tls_options.remove_class("hidden")
            else:
                tls_options.add_class("hidden")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "cancel":
            self.dismiss(None)
        elif event.button.id == "connect":
            result = self._get_connection_result()
            # Save profile if requested
            if result.save_profile and result.profile_name:
                self._save_profile(result)
            self.dismiss(result)
        elif event.button.id == "test":
            self._test_connection()

    def action_cancel(self) -> None:
        """Cancel the dialog."""
        self.dismiss(None)

    def _get_connection_result(self) -> ConnectionResult:
        """Get the connection configuration from inputs."""
        server_url = self.query_one("#server_url", Input).value.strip()
        username = self.query_one("#username", Input).value.strip() or None
        password = self.query_one("#password", Input).value or None
        tls_enabled = self.query_one("#tls_enabled", Checkbox).value
        tls_ca_cert = self.query_one("#tls_ca_cert", Input).value.strip() or None
        tls_cert = self.query_one("#tls_cert", Input).value.strip() or None
        tls_key = self.query_one("#tls_key", Input).value.strip() or None
        tls_insecure = self.query_one("#tls_insecure", Checkbox).value
        save_profile = self.query_one("#save_profile", Checkbox).value
        profile_name = self.query_one("#profile_name", Input).value.strip() or None

        # Auto-enable TLS if server URL starts with tls://
        if server_url.startswith("tls://"):
            tls_enabled = True

        return ConnectionResult(
            server_url=server_url,
            username=username,
            password=password,
            tls_enabled=tls_enabled,
            tls_ca_cert=tls_ca_cert,
            tls_cert=tls_cert,
            tls_key=tls_key,
            tls_insecure=tls_insecure,
            save_profile=save_profile,
            profile_name=profile_name,
        )

    def _save_profile(self, result: ConnectionResult) -> None:
        """Save the connection as a profile."""
        if not result.profile_name:
            return

        profile: ConnectionProfile = {"server": result.server_url}
        if result.username:
            profile["username"] = result.username
        if result.password:
            profile["password"] = result.password
        if result.tls_enabled:
            profile["tls"] = True
        if result.tls_ca_cert:
            profile["tls_ca_cert"] = result.tls_ca_cert
        if result.tls_cert:
            profile["tls_cert"] = result.tls_cert
        if result.tls_key:
            profile["tls_key"] = result.tls_key
        if result.tls_insecure:
            profile["tls_insecure"] = True

        self._config.profiles[result.profile_name] = profile
        save_config(self._config)
        self.notify(f"Profile '{result.profile_name}' saved", severity="information")

    @work(thread=True, exclusive=True, group="test_connection")
    async def _test_connection(self) -> None:
        """Test the connection in a background worker."""
        try:
            result = self._get_connection_result()

            # Perform the test
            config = ConnectionConfig(
                server_url=result.server_url,
                username=result.username,
                password=result.password,
                tls_enabled=result.tls_enabled,
                tls_ca_cert=result.tls_ca_cert,
                tls_cert=result.tls_cert,
                tls_key=result.tls_key,
                tls_insecure=result.tls_insecure,
            )
            adapter = NatsAdapter(config)
            success, message = await adapter.test_connection()

            # Update UI with result using app's call_from_thread for thread safety
            def update_ui():
                try:
                    test_label = self.query_one("#test_result", Static)
                    test_label.update(message)
                    test_label.remove_class("success", "error")
                    test_label.add_class("success" if success else "error")
                except Exception:
                    pass  # Dialog might be closing

            self.app.call_from_thread(update_ui)

        except Exception as e:
            # Handle any unexpected errors
            def show_error():
                try:
                    test_label = self.query_one("#test_result", Static)
                    test_label.update(f"Error: {e}")
                    test_label.remove_class("success")
                    test_label.add_class("error")
                except Exception:
                    pass  # Dialog might be closing

            self.app.call_from_thread(show_error)
