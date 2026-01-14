"""CLI entry point for NATS TUI using rich-click."""

from pathlib import Path

import rich_click as click

from nats_tui.colors import DEFAULT_THEME, GREEN, PINK, VALID_THEMES, YELLOW
from nats_tui.config import get_profile, load_config
from nats_tui.exception import NatsTuiConfigError, pretty_error_message

# Build list of available themes for help text
ALL_THEMES = ", ".join(sorted(VALID_THEMES.keys()))

# Rich-click styling
click.rich_click.USE_RICH_MARKUP = True
click.rich_click.COLOR_SYSTEM = "truecolor"
click.rich_click.STYLE_OPTIONS_PANEL_BORDER = YELLOW
click.rich_click.STYLE_USAGE = f"bold {YELLOW}"
click.rich_click.STYLE_OPTION = PINK
click.rich_click.STYLE_ARGUMENT = PINK
click.rich_click.STYLE_SWITCH = GREEN

click.rich_click.OPTION_GROUPS = {
    "nats-tui": [
        {"name": "Connection", "options": ["--server", "--profile", "--username", "--password"]},
        {
            "name": "TLS",
            "options": [
                "--tls",
                "--tls-ca-cert",
                "--tls-cert",
                "--tls-key",
                "--tls-insecure",
            ],
        },
        {"name": "Configuration", "options": ["--config", "--theme"]},
        {"name": "Info", "options": ["--version", "--help"]},
    ]
}


@click.command()
@click.version_option(package_name="nats-tui")
@click.option(
    "-s",
    "--server",
    default=None,
    help="NATS server URL (e.g., nats://localhost:4222 or tls://localhost:4222)",
)
@click.option(
    "-P",
    "--profile",
    default=None,
    help="Connection profile name from config file",
)
@click.option(
    "-u",
    "--username",
    default=None,
    help="Username for NATS authentication",
)
@click.option(
    "-p",
    "--password",
    default=None,
    help="Password for NATS authentication",
)
@click.option(
    "--tls",
    "tls_enabled",
    is_flag=True,
    default=False,
    help="Enable TLS connection",
)
@click.option(
    "--tls-ca-cert",
    default=None,
    type=click.Path(exists=False, path_type=Path),
    help="Path to CA certificate file for TLS verification",
)
@click.option(
    "--tls-cert",
    default=None,
    type=click.Path(exists=False, path_type=Path),
    help="Path to client certificate file (for mutual TLS)",
)
@click.option(
    "--tls-key",
    default=None,
    type=click.Path(exists=False, path_type=Path),
    help="Path to client key file (for mutual TLS)",
)
@click.option(
    "--tls-insecure",
    is_flag=True,
    default=False,
    help="Disable TLS certificate verification (insecure)",
)
@click.option(
    "-c",
    "--config",
    "config_path",
    default=None,
    type=click.Path(exists=False, path_type=Path),
    help="Path to config file (TOML)",
)
@click.option(
    "-t",
    "--theme",
    default=None,
    help=f"Theme name. Available: {ALL_THEMES}",
)
def nats_tui(
    server: str | None,
    profile: str | None,
    username: str | None,
    password: str | None,
    tls_enabled: bool,
    tls_ca_cert: Path | None,
    tls_cert: Path | None,
    tls_key: Path | None,
    tls_insecure: bool,
    config_path: Path | None,
    theme: str | None,
) -> None:
    """A terminal UI for NATS cluster management.

    Connection profiles can be saved in ~/.config/nats-tui/config.toml or
    a local .nats-tui.toml file.

    Example config with TLS and auth:

    \b
        [profiles.prod]
        server = "tls://prod.example.com:4222"
        username = "admin"
        password = "secret"
        tls = true
        tls_ca_cert = "/path/to/ca.crt"
        tls_insecure = false

    \b
        [profiles.dev]
        server = "tls://dev.example.com:4222"
        tls = true
        tls_ca_cert = "/path/to/ca.crt"
        tls_insecure = true  # For self-signed certs

    Example usage:

    \b
        # Connect with authentication
        nats-tui -s nats://server:4222 -u admin -p secret

    \b
        # Connect with TLS and auth
        nats-tui -s tls://server:4222 --tls-ca-cert /path/to/ca.crt -u admin -p secret

    \b
        # Connect with TLS but skip verification (for self-signed certs)
        nats-tui -s tls://server:4222 --tls-ca-cert /path/to/ca.crt --tls-insecure -u admin -p secret

    \b
        # Launch TUI without auto-connecting (configure in dialog)
        nats-tui

    \b
        # Mutual TLS with client certificate
        nats-tui -s tls://server:4222 --tls --tls-ca-cert ca.crt --tls-cert client.crt --tls-key client.key
    """
    from rich.console import Console

    from nats_tui.app import NatsTuiApp

    console = Console()

    # Load configuration
    try:
        config = load_config(config_path)
    except NatsTuiConfigError as e:
        console.print(pretty_error_message(e))
        raise SystemExit(1) from e

    # Determine server URL and TLS settings (CLI > profile > None)
    server_url = server
    profile_data = None

    # TLS and auth settings from CLI
    tls_config = {
        "tls_enabled": tls_enabled,
        "tls_ca_cert": str(tls_ca_cert) if tls_ca_cert else None,
        "tls_cert": str(tls_cert) if tls_cert else None,
        "tls_key": str(tls_key) if tls_key else None,
        "tls_insecure": tls_insecure,
        "username": username,
        "password": password,
    }

    if profile or (server is None and config.default_profile):
        try:
            profile_data = get_profile(config, profile)
            if profile_data:
                if not server_url:
                    server_url = profile_data.get("server")
                # Use profile TLS settings if CLI didn't override
                if not tls_enabled and profile_data.get("tls"):
                    tls_config["tls_enabled"] = True
                if not tls_ca_cert and profile_data.get("tls_ca_cert"):
                    tls_config["tls_ca_cert"] = profile_data.get("tls_ca_cert")
                if not tls_cert and profile_data.get("tls_cert"):
                    tls_config["tls_cert"] = profile_data.get("tls_cert")
                if not tls_key and profile_data.get("tls_key"):
                    tls_config["tls_key"] = profile_data.get("tls_key")
                if not tls_insecure and profile_data.get("tls_insecure"):
                    tls_config["tls_insecure"] = profile_data.get("tls_insecure")
                # Use profile auth settings if CLI didn't override
                if not username and profile_data.get("username"):
                    tls_config["username"] = profile_data.get("username")
                if not password and profile_data.get("password"):
                    tls_config["password"] = profile_data.get("password")
        except NatsTuiConfigError as e:
            console.print(pretty_error_message(e))
            raise SystemExit(1) from e

    # Auto-enable TLS if server URL starts with tls:// or any TLS option is set
    if server_url and server_url.startswith("tls://"):
        tls_config["tls_enabled"] = True
    if tls_ca_cert or tls_cert or tls_key:
        tls_config["tls_enabled"] = True

    # Determine theme (CLI > config > default)
    effective_theme = theme or config.theme or DEFAULT_THEME

    app = NatsTuiApp(
        theme=effective_theme,
        server_url=server_url,
        config=config,
        profile_data=profile_data,
        tls_config=tls_config,
    )
    try:
        app.run()
    except AttributeError as e:
        # Workaround for Textual shutdown bug in some versions
        # https://github.com/Textualize/textual/issues/
        if "_clear" in str(e):
            pass  # Ignore the shutdown error
        else:
            raise
