"""Dialog for creating a new Object Store."""

import re
from dataclasses import dataclass

from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Select


def parse_duration(value: str) -> float:
    """Parse a duration string like '1d', '4h', '30m', '10s' to seconds."""
    if not value or value.strip() == "" or value.strip() == "0":
        return 0

    value = value.strip().lower()

    try:
        return float(value)
    except ValueError:
        pass

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
    """Parse a size string like '1mb', '256kb', '1gb' to bytes."""
    if not value or value.strip() == "" or value.strip() == "-1":
        return -1

    value = value.strip().lower()

    try:
        return int(value)
    except ValueError:
        pass

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
class CreateObjectStoreResult:
    """Result from create object store dialog."""

    name: str
    description: str
    storage: str  # "file" or "memory"
    replicas: int
    max_bytes: int  # -1 = unlimited
    ttl: float  # seconds, 0 = no TTL


class CreateObjectStoreDialog(ModalScreen[CreateObjectStoreResult | None]):
    """Dialog for creating a new object store."""

    DEFAULT_CSS = """
    CreateObjectStoreDialog {
        align: center middle;
    }

    #create_object_store_dialog {
        width: 70;
        height: auto;
        max-height: 80%;
        border: thick $primary;
        background: $surface;
        padding: 1 2;
    }

    #create_object_store_title {
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

    #create_object_store_dialog Input {
        width: 100%;
    }

    #create_object_store_dialog Select {
        width: 100%;
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
        with VerticalScroll(id="create_object_store_dialog"):
            yield Label("Create Object Store", id="create_object_store_title")

            # Basic settings
            yield Label("Store Name:", classes="field_label")
            yield Input(placeholder="my-store", id="store_name")

            yield Label("Description (optional):", classes="field_label")
            yield Input(placeholder="Description of the object store", id="store_description")

            # Storage Type
            yield Label("Storage Type:", classes="field_label")
            yield Select(
                [("File (persistent)", "file"), ("Memory (fast)", "memory")],
                value="file",
                id="store_storage",
            )

            # Replication
            yield Label("Replicas (1-5, for clustering):", classes="field_label")
            yield Select(
                [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")],
                value="1",
                id="store_replicas",
            )

            # Limits
            yield Label("Max Size (e.g., 256mb, 1gb, -1 = unlimited):", classes="field_label")
            yield Input(placeholder="-1", value="-1", id="max_bytes")

            yield Label("TTL (e.g., 1d, 4h, 0 = no TTL):", classes="field_label")
            yield Input(placeholder="0", value="0", id="store_ttl")
            yield Label("Objects expire after this time", classes="field_hint")

            with Horizontal(id="button_row"):
                yield Button("Cancel", variant="default", id="cancel_btn")
                yield Button("Create", variant="primary", id="create_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "cancel_btn":
            self.dismiss(None)
        elif event.button.id == "create_btn":
            self._create_store()

    def _create_store(self) -> None:
        """Validate and create object store."""
        name = self.query_one("#store_name", Input).value.strip()
        description = self.query_one("#store_description", Input).value.strip()
        storage = str(self.query_one("#store_storage", Select).value)
        replicas = int(self.query_one("#store_replicas", Select).value)
        max_bytes_str = self.query_one("#max_bytes", Input).value.strip()
        ttl_str = self.query_one("#store_ttl", Input).value.strip()

        # Validate required fields
        if not name:
            self.notify("Store name is required", severity="error")
            return

        # Validate name format (alphanumeric, dash, underscore)
        if not re.match(r'^[a-zA-Z0-9_-]+$', name):
            self.notify("Store name must be alphanumeric (dash/underscore allowed)", severity="error")
            return

        max_bytes = parse_size(max_bytes_str)
        ttl = parse_duration(ttl_str)

        self.dismiss(
            CreateObjectStoreResult(
                name=name,
                description=description,
                storage=storage,
                replicas=replicas,
                max_bytes=max_bytes,
                ttl=ttl,
            )
        )

    def action_cancel(self) -> None:
        """Cancel the dialog."""
        self.dismiss(None)
