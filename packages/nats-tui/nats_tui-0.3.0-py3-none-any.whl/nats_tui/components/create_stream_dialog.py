"""Dialog for creating a new JetStream stream."""

import re
from dataclasses import dataclass

from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Select, Switch


def parse_duration(value: str) -> float:
    """Parse a duration string like '1d', '4h', '30m', '10s' to seconds.

    Args:
        value: Duration string (e.g., '1d', '4h', '30m', '10s', '100ms')

    Returns:
        Duration in seconds as float, or 0 if invalid/empty
    """
    if not value or value.strip() == "" or value.strip() == "0":
        return 0

    value = value.strip().lower()

    # Try to parse as plain number (seconds)
    try:
        return float(value)
    except ValueError:
        pass

    # Parse duration with unit
    match = re.match(r'^(\d+(?:\.\d+)?)\s*(d|h|m|s|ms)?$', value)
    if not match:
        return 0

    num = float(match.group(1))
    unit = match.group(2) or 's'

    multipliers = {
        'ms': 0.001,
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400,
    }

    return num * multipliers.get(unit, 1)


def parse_size(value: str) -> int:
    """Parse a size string like '1mb', '256kb', '1gb' to bytes.

    Args:
        value: Size string (e.g., '1mb', '256kb', '1gb') or plain number

    Returns:
        Size in bytes as int, or -1 if invalid/empty/unlimited
    """
    if not value or value.strip() == "" or value.strip() == "-1":
        return -1

    value = value.strip().lower()

    # Try to parse as plain number (bytes)
    try:
        return int(value)
    except ValueError:
        pass

    # Parse size with unit
    match = re.match(r'^(\d+(?:\.\d+)?)\s*(b|kb|mb|gb|tb)?$', value)
    if not match:
        return -1

    num = float(match.group(1))
    unit = match.group(2) or 'b'

    multipliers = {
        'b': 1,
        'kb': 1024,
        'mb': 1024 * 1024,
        'gb': 1024 * 1024 * 1024,
        'tb': 1024 * 1024 * 1024 * 1024,
    }

    return int(num * multipliers.get(unit, 1))


@dataclass
class CreateStreamResult:
    """Result from create stream dialog."""

    name: str
    subjects: list[str]
    storage: str  # "file" or "memory"
    retention: str  # "limits", "interest", "workqueue"
    discard: str  # "old" or "new"
    max_msgs: int  # -1 = unlimited
    max_bytes: int  # -1 = unlimited
    max_age: float  # seconds, 0 = unlimited
    max_msg_size: int  # -1 = unlimited
    max_msgs_per_subject: int  # -1 = unlimited
    num_replicas: int  # 1-5
    duplicate_window: float  # seconds
    allow_rollup: bool
    deny_delete: bool
    deny_purge: bool


class CreateStreamDialog(ModalScreen[CreateStreamResult | None]):
    """Dialog for creating a new stream with full configuration options."""

    DEFAULT_CSS = """
    CreateStreamDialog {
        align: center middle;
    }

    #create_stream_dialog {
        width: 80;
        height: auto;
        max-height: 90%;
        border: thick $primary;
        background: $surface;
        padding: 1 2;
    }

    #create_stream_title {
        text-align: center;
        text-style: bold;
        width: 100%;
        margin-bottom: 1;
    }

    .field_label {
        margin-top: 1;
        color: $text-muted;
    }

    .field_hint {
        color: $text-disabled;
        text-style: italic;
    }

    #create_stream_dialog Input {
        width: 100%;
    }

    #create_stream_dialog Select {
        width: 100%;
    }

    .switch_row {
        height: auto;
        width: 100%;
        margin-top: 1;
    }

    .switch_row Label {
        width: 1fr;
    }

    .switch_row Switch {
        width: auto;
    }

    #button_row {
        height: auto;
        align: center middle;
        margin-top: 2;
    }

    #button_row Button {
        margin: 0 2;
    }
    """

    BINDINGS = [("escape", "cancel", "Cancel")]

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        with VerticalScroll(id="create_stream_dialog"):
            yield Label("Create Stream", id="create_stream_title")

            # Basic settings
            yield Label("Stream Name:", classes="field_label")
            yield Input(placeholder="my-stream", id="stream_name")

            yield Label("Subjects (comma-separated, wildcards supported):", classes="field_label")
            yield Input(placeholder="orders.>, events.*, jobs.*.*", id="stream_subjects")
            yield Label("Use > for all, * for single token wildcard", classes="field_hint")

            # Storage and Retention
            yield Label("Storage Type:", classes="field_label")
            yield Select(
                [("File (persistent)", "file"), ("Memory (fast)", "memory")],
                value="file",
                id="stream_storage",
            )

            yield Label("Retention Policy:", classes="field_label")
            yield Select(
                [
                    ("Limits (keep until limits reached)", "limits"),
                    ("Interest (keep while consumers exist)", "interest"),
                    ("Work Queue (remove after ack)", "workqueue"),
                ],
                value="limits",
                id="stream_retention",
            )

            yield Label("Discard Policy (when limits reached):", classes="field_label")
            yield Select(
                [
                    ("Old (discard oldest messages)", "old"),
                    ("New (reject new messages)", "new"),
                ],
                value="old",
                id="stream_discard",
            )

            # Replication
            yield Label("Replicas (1-5, for clustering):", classes="field_label")
            yield Select(
                [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")],
                value="1",
                id="stream_replicas",
            )

            # Limits
            yield Label("Max Messages (-1 = unlimited):", classes="field_label")
            yield Input(placeholder="-1", value="-1", id="max_msgs")

            yield Label("Max Messages Per Subject (-1 = unlimited):", classes="field_label")
            yield Input(placeholder="-1", value="-1", id="max_msgs_per_subject")

            yield Label("Total Stream Size (e.g., 256mb, 1gb, -1 = unlimited):", classes="field_label")
            yield Input(placeholder="256mb", value="-1", id="max_bytes")

            yield Label("Max Message Size (e.g., 1mb, -1 = unlimited):", classes="field_label")
            yield Input(placeholder="1mb", value="-1", id="max_msg_size")

            yield Label("Message TTL (e.g., 1d, 4h, 30m, 0 = unlimited):", classes="field_label")
            yield Input(placeholder="0", value="0", id="max_age")

            yield Label("Duplicate Window (e.g., 2m, 0 = disabled):", classes="field_label")
            yield Input(placeholder="2m", value="0", id="duplicate_window")

            # Boolean options
            with Horizontal(classes="switch_row"):
                yield Label("Allow Message Roll-ups:")
                yield Switch(value=False, id="allow_rollup")

            with Horizontal(classes="switch_row"):
                yield Label("Allow Message Deletion:")
                yield Switch(value=True, id="allow_delete")

            with Horizontal(classes="switch_row"):
                yield Label("Allow Purging:")
                yield Switch(value=True, id="allow_purge")

            with Horizontal(id="button_row"):
                yield Button("Cancel", variant="default", id="cancel_btn")
                yield Button("Create", variant="primary", id="create_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "cancel_btn":
            self.dismiss(None)
        elif event.button.id == "create_btn":
            self._create_stream()

    def _create_stream(self) -> None:
        """Validate and create stream."""
        # Get basic values
        name = self.query_one("#stream_name", Input).value.strip()
        subjects_raw = self.query_one("#stream_subjects", Input).value.strip()
        subjects = [s.strip() for s in subjects_raw.split(",") if s.strip()]

        # Get select values
        storage = str(self.query_one("#stream_storage", Select).value)
        retention = str(self.query_one("#stream_retention", Select).value)
        discard = str(self.query_one("#stream_discard", Select).value)
        replicas = int(self.query_one("#stream_replicas", Select).value)

        # Get numeric values
        max_msgs_str = self.query_one("#max_msgs", Input).value.strip()
        max_msgs_per_subject_str = self.query_one("#max_msgs_per_subject", Input).value.strip()
        max_bytes_str = self.query_one("#max_bytes", Input).value.strip()
        max_msg_size_str = self.query_one("#max_msg_size", Input).value.strip()
        max_age_str = self.query_one("#max_age", Input).value.strip()
        duplicate_window_str = self.query_one("#duplicate_window", Input).value.strip()

        # Get boolean values
        allow_rollup = self.query_one("#allow_rollup", Switch).value
        allow_delete = self.query_one("#allow_delete", Switch).value
        allow_purge = self.query_one("#allow_purge", Switch).value

        # Validate required fields
        if not name:
            self.notify("Stream name is required", severity="error")
            return
        if not subjects:
            self.notify("At least one subject is required", severity="error")
            return

        # Parse numeric values
        try:
            max_msgs = int(max_msgs_str) if max_msgs_str else -1
        except ValueError:
            self.notify("Max messages must be a number", severity="error")
            return

        try:
            max_msgs_per_subject = int(max_msgs_per_subject_str) if max_msgs_per_subject_str else -1
        except ValueError:
            self.notify("Max messages per subject must be a number", severity="error")
            return

        max_bytes = parse_size(max_bytes_str)
        max_msg_size = parse_size(max_msg_size_str)
        max_age = parse_duration(max_age_str)
        duplicate_window = parse_duration(duplicate_window_str)

        self.dismiss(
            CreateStreamResult(
                name=name,
                subjects=subjects,
                storage=storage,
                retention=retention,
                discard=discard,
                max_msgs=max_msgs,
                max_bytes=max_bytes,
                max_age=max_age,
                max_msg_size=max_msg_size,
                max_msgs_per_subject=max_msgs_per_subject,
                num_replicas=replicas,
                duplicate_window=duplicate_window,
                allow_rollup=allow_rollup,
                deny_delete=not allow_delete,  # Invert for API
                deny_purge=not allow_purge,  # Invert for API
            )
        )

    def action_cancel(self) -> None:
        """Cancel the dialog."""
        self.dismiss(None)
