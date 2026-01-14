"""TOML configuration handling for NATS TUI."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TypedDict

from platformdirs import user_config_path
from tomlkit.exceptions import TOMLKitError
from tomlkit.toml_document import TOMLDocument
from tomlkit.toml_file import TOMLFile

from nats_tui.exception import NatsTuiConfigError


class ConnectionProfile(TypedDict, total=False):
    """Connection profile configuration."""

    server: str
    username: str
    password: str
    theme: str
    # TLS options
    tls: bool
    tls_ca_cert: str
    tls_cert: str
    tls_key: str
    tls_insecure: bool


class KeyBinding(TypedDict, total=False):
    """Key binding configuration."""

    keys: str
    action: str


class Config(TypedDict, total=False):
    """Top-level configuration."""

    default_profile: str | None
    theme: str | None
    profiles: dict[str, ConnectionProfile]
    keybindings: dict[str, str]  # action -> keys


@dataclass
class NatsTuiConfig:
    """Loaded configuration with defaults applied."""

    default_profile: str | None = None
    theme: str = "nats-tui"
    profiles: dict[str, ConnectionProfile] = field(default_factory=dict)
    keybindings: dict[str, str] = field(default_factory=dict)

    def get_profile(self, name: str | None) -> ConnectionProfile | None:
        """Get a profile by name, or None if not found."""
        if name is None:
            name = self.default_profile
        if name is None:
            return None
        return self.profiles.get(name)

    def save_profile(
        self,
        name: str,
        server: str,
        username: str | None = None,
        password: str | None = None,
    ) -> None:
        """Save or update a connection profile."""
        profile: ConnectionProfile = {"server": server}
        if username:
            profile["username"] = username
        if password:
            profile["password"] = password
        self.profiles[name] = profile


class ConfigFile:
    """Handles reading and writing TOML config files."""

    def __init__(self, path: Path) -> None:
        """Open and read a TOML config file.

        Args:
            path: Path to the config file

        Raises:
            NatsTuiConfigError: If the file exists but cannot be parsed
        """
        self.path = path
        self.toml_file = TOMLFile(path)
        self.is_pyproject = path.name == "pyproject.toml"

        try:
            if path.exists():
                self.toml_doc = self.toml_file.read()
            else:
                self.toml_doc = TOMLDocument()
        except TOMLKitError as e:
            raise NatsTuiConfigError(
                f"Could not parse config file at {path}:\n{e}",
                title="Configuration Error",
            ) from e

    @property
    def relevant_config(self) -> Config:
        """Get the relevant config section from the file."""
        raw = self.toml_doc.unwrap()
        if self.is_pyproject:
            return raw.get("tool", {}).get("nats-tui", {})
        return raw

    def update(self, config: Config) -> None:
        """Update the config file with new values."""
        if self.is_pyproject:
            if "tool" not in self.toml_doc:
                self.toml_doc["tool"] = {"nats-tui": {}}
            elif "nats-tui" not in self.toml_doc["tool"]:  # type: ignore
                self.toml_doc["tool"]["nats-tui"] = {}  # type: ignore
            self.toml_doc["tool"]["nats-tui"].update(config)  # type: ignore
        else:
            self.toml_doc.update(config)

    def write(self) -> None:
        """Write the config to disk."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.toml_file.write(self.toml_doc)


def get_config_dir() -> Path:
    """Get the user config directory for nats-tui."""
    return user_config_path(appname="nats-tui", appauthor=False)


def get_default_config_path() -> Path:
    """Get the default config file path."""
    return get_config_dir() / "config.toml"


def find_config_files(config_path: Path | None = None) -> list[Path]:
    """Find all config files to load, in priority order (lowest first).

    Searches:
    1. ~/.config/nats-tui/config.toml (or platform equivalent)
    2. ./pyproject.toml (if has [tool.nats-tui] section)
    3. ./.nats-tui.toml
    4. ./nats-tui.toml
    5. Explicitly provided config_path (highest priority)
    """
    found: list[Path] = []

    # User config directory
    user_config = get_config_dir()
    for filename in ["config.toml", ".nats-tui.toml", "nats-tui.toml"]:
        path = user_config / filename
        if path.exists():
            found.append(path)

    # Current directory
    cwd = Path.cwd()
    for filename in ["pyproject.toml", ".nats-tui.toml", "nats-tui.toml"]:
        path = cwd / filename
        if path.exists():
            # For pyproject.toml, only include if it has our section
            if filename == "pyproject.toml":
                try:
                    cf = ConfigFile(path)
                    if cf.relevant_config:
                        found.append(path)
                except NatsTuiConfigError:
                    pass
            else:
                found.append(path)

    # Explicit config path has highest priority
    if config_path is not None:
        if config_path.exists():
            found.append(config_path)
        else:
            raise NatsTuiConfigError(
                f"Config file not found: {config_path}",
                title="Configuration Error",
            )

    return found


def load_config(config_path: Path | None = None) -> NatsTuiConfig:
    """Load configuration from all discovered config files.

    Files are loaded in priority order, with later files overriding earlier ones.

    Args:
        config_path: Optional explicit config file path

    Returns:
        Merged NatsTuiConfig
    """
    paths = find_config_files(config_path)
    merged: Config = {}

    for path in paths:
        try:
            cf = ConfigFile(path)
            config = cf.relevant_config
            # Deep merge profiles
            if "profiles" in config:
                existing_profiles = merged.get("profiles", {})
                existing_profiles.update(config["profiles"])
                merged["profiles"] = existing_profiles
            # Deep merge keybindings
            if "keybindings" in config:
                existing_keybindings = merged.get("keybindings", {})
                existing_keybindings.update(config["keybindings"])
                merged["keybindings"] = existing_keybindings
            # Shallow merge other keys
            for key in ["default_profile", "theme"]:
                if key in config:
                    merged[key] = config[key]  # type: ignore
        except NatsTuiConfigError:
            # Skip files that can't be loaded
            pass

    return NatsTuiConfig(
        default_profile=merged.get("default_profile"),
        theme=merged.get("theme", "nats-tui"),
        profiles=merged.get("profiles", {}),
        keybindings=merged.get("keybindings", {}),
    )


def save_config(config: NatsTuiConfig, path: Path | None = None) -> None:
    """Save configuration to a file.

    Args:
        config: Configuration to save
        path: Path to save to (defaults to user config dir)
    """
    if path is None:
        path = get_default_config_path()

    # Build config dict
    config_dict: Config = {}
    if config.default_profile:
        config_dict["default_profile"] = config.default_profile
    if config.theme != "nats-tui":
        config_dict["theme"] = config.theme
    if config.profiles:
        config_dict["profiles"] = config.profiles
    if config.keybindings:
        config_dict["keybindings"] = config.keybindings

    cf = ConfigFile(path)
    cf.update(config_dict)
    cf.write()


def get_profile(
    config: NatsTuiConfig, profile_name: str | None
) -> ConnectionProfile | None:
    """Get a connection profile by name.

    Args:
        config: Loaded configuration
        profile_name: Profile name, or None to use default

    Returns:
        ConnectionProfile or None if not found
    """
    name = profile_name or config.default_profile
    if name is None:
        return None
    if name not in config.profiles:
        raise NatsTuiConfigError(
            f"Profile '{name}' not found in configuration.\n"
            f"Available profiles: {', '.join(config.profiles.keys()) or 'none'}",
            title="Profile Not Found",
        )
    return config.profiles[name]
