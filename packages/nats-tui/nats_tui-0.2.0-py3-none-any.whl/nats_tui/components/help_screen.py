"""Help screen modal for NATS TUI."""

from textual import events
from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Markdown, Static

from nats_tui.keymap import ACTION_DESCRIPTIONS, DEFAULT_KEYBINDINGS

# Help content as markdown
HELP_MARKDOWN = """
# NATS TUI Help

A terminal UI for NATS cluster management.

## Key Bindings

### Global
| Key | Action |
|-----|--------|
| `q` | Quit the application |
| `?` / `F1` | Show this help |
| `c` | Open connection dialog |
| `d` | Disconnect from server |
| `r` | Refresh current view |

### Navigation
| Key | Action |
|-----|--------|
| `Escape` | Go back to previous view |
| `Enter` | View consumers (in stream view) |
| `j` | Switch to JetStream view |

### Subject Browser
| Key | Action |
|-----|--------|
| `p` | Publish message to subject |
| `s` | Subscribe to subject |
| `u` | Unsubscribe |
| `x` | Clear discovered subjects |

### JetStream
| Key | Action |
|-----|--------|
| `n` | Create new stream/consumer |
| `m` | View messages in selected stream |
| `Delete` | Delete selected stream/consumer/message |
| `Shift+P` | Purge selected stream |
| `Space` | Pause/resume consumer |

### Stream Messages View
| Key | Action |
|-----|--------|
| `j` | Return to JetStream stream list |
| `Delete` | Delete selected message |
| `Shift+P` | Purge all messages from stream |
| `Escape` | Go back to stream list |

**Note:** All delete and purge actions show a confirmation dialog.

## Configuration

Config files are loaded from (in order of priority):
1. `~/.config/nats-tui/config.toml`
2. `./pyproject.toml` (under `[tool.nats-tui]`)
3. `./.nats-tui.toml`
4. `./nats-tui.toml`

### Example Config

```toml
default_profile = "prod"
theme = "nats-tui-light"

[profiles.local]
server = "nats://localhost:4222"

[profiles.prod]
server = "tls://prod.example.com:4222"
username = "admin"
password = "secret"
tls = true
tls_ca_cert = "/path/to/ca.crt"

[profiles.dev]
server = "tls://dev.example.com:4222"
tls = true
tls_ca_cert = "/path/to/ca.crt"
tls_insecure = true  # Skip verification for self-signed certs
```

## TLS Configuration

nats-tui supports TLS connections with the following options:

| Option | Description |
|--------|-------------|
| `--tls` | Enable TLS connection |
| `--tls-ca-cert` | Path to CA certificate file |
| `--tls-cert` | Path to client certificate (mutual TLS) |
| `--tls-key` | Path to client key (mutual TLS) |
| `--tls-insecure` | Skip certificate verification |

TLS is auto-enabled when using `tls://` server URLs.

## Command Line Options

```
nats-tui [OPTIONS]

Connection:
  -s, --server URL      NATS server URL
  -P, --profile NAME    Connection profile name
  -u, --username USER   Username for authentication
  -p, --password PASS   Password for authentication

TLS:
  --tls                 Enable TLS
  --tls-ca-cert PATH    CA certificate file
  --tls-cert PATH       Client certificate (mTLS)
  --tls-key PATH        Client key (mTLS)
  --tls-insecure        Skip cert verification

Configuration:
  -c, --config PATH     Config file path
  -t, --theme NAME      Theme name (see below)

Info:
  --version             Show version
  --help                Show help
```

### Examples

```bash
# Connect with username/password
nats-tui -s nats://localhost:4222 -u admin -p secret

# Connect with TLS and auth
nats-tui -s tls://server:4222 --tls-ca-cert ca.crt -u admin -p secret

# Use a saved profile
nats-tui -P prod

# Use a different theme
nats-tui -t dracula
```

## Available Themes

**OSCAR themes:**
- `oscar` (default) - Yellow primary, EDS color palette
- `oscar-light` - Light mode variant

**NATS themes:**
- `nats-tui` - Green primary (original)
- `nats-tui-light` - Light mode variant

**Built-in:** dracula, monokai, nord, gruvbox, tokyo-night,
catppuccin-mocha, catppuccin-latte, solarized-dark, solarized-light,
atom-one-dark, atom-one-light, rose-pine, flexoki, and more.

Set theme via CLI (`-t NAME`) or config file (`theme = "NAME"`).

### Defining Custom Themes

Custom themes are defined in `src/nats_tui/colors.py` using
Textual's Theme class. Each theme specifies colors for:

- `primary` - Main UI elements (borders, highlights)
- `secondary` - Secondary accents
- `warning` - Warning messages
- `error` - Error messages and destructive actions
- `success` - Success indicators
- `foreground` - Text color
- `background` - Main background
- `surface` - Panel/card backgrounds

## More Information

- GitHub: https://github.com/coreyellis/nats-tui
- NATS: https://nats.io
"""


class HelpScreen(ModalScreen):
    """Modal screen showing help information."""

    DEFAULT_CSS = """
    HelpScreen {
        align: center middle;
    }

    #help_outer {
        width: 80;
        height: 80%;
        border: thick $primary;
        background: $surface;
    }

    #help_header {
        dock: top;
        height: 1;
        padding: 0 1;
        background: $primary;
        color: $text;
        text-style: bold;
    }

    #help_inner {
        padding: 1 2;
    }

    #help_footer {
        dock: bottom;
        height: 1;
        padding: 0 1;
        background: $primary-darken-2;
        color: $text-muted;
        text-align: center;
    }
    """

    def compose(self) -> ComposeResult:
        """Create the help screen widgets."""
        with Vertical(id="help_outer"):
            yield Static("NATS TUI Help", id="help_header")
            with VerticalScroll(id="help_inner"):
                yield Markdown(HELP_MARKDOWN)
            yield Static(
                "Scroll with arrows/PageUp/PageDown. Press any other key to close.",
                id="help_footer",
            )

    def on_mount(self) -> None:
        """Set up the help screen."""
        self._scroll_container = self.query_one("#help_inner", VerticalScroll)

    def on_key(self, event: events.Key) -> None:
        """Handle key events."""
        event.stop()
        if event.key == "up":
            self._scroll_container.scroll_up()
        elif event.key == "down":
            self._scroll_container.scroll_down()
        elif event.key == "pageup":
            self._scroll_container.scroll_page_up()
        elif event.key == "pagedown":
            self._scroll_container.scroll_page_down()
        elif event.key == "home":
            self._scroll_container.scroll_home()
        elif event.key == "end":
            self._scroll_container.scroll_end()
        else:
            self.app.pop_screen()

    def on_click(self) -> None:
        """Close on click outside content."""
        self.app.pop_screen()
