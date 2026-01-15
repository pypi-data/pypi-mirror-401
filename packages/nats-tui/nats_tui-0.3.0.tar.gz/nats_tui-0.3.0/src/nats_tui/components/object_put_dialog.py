"""Dialog for uploading an object to an Object Store."""

from dataclasses import dataclass
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, TextArea


@dataclass
class ObjectPutResult:
    """Result from object put dialog."""

    name: str
    description: str
    data: bytes
    from_file: bool  # True if loaded from file, False if manual input


class ObjectPutDialog(ModalScreen[ObjectPutResult | None]):
    """Dialog for uploading an object to a store."""

    DEFAULT_CSS = """
    ObjectPutDialog {
        align: center middle;
    }

    #object_put_dialog {
        width: 80;
        height: auto;
        max-height: 85%;
        border: thick $primary;
        background: $surface;
        padding: 1 2;
    }

    #object_put_title {
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

    #object_put_dialog Input {
        width: 100%;
    }

    #object_put_dialog TextArea {
        width: 100%;
        height: 10;
    }

    .or_separator {
        text-align: center;
        color: $text-muted;
        margin: 1 0;
    }

    #button_row {
        height: auto;
        align: center middle;
        margin-top: 2;
    }

    #button_row Button {
        margin: 0 2;
    }

    #load_file_btn {
        margin-top: 1;
    }

    #file_status {
        margin-top: 1;
        color: $success;
    }
    """

    BINDINGS = [("escape", "cancel", "Cancel")]

    def __init__(self, store_name: str) -> None:
        super().__init__()
        self._store_name = store_name
        self._file_data: bytes | None = None
        self._file_name: str | None = None

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        with VerticalScroll(id="object_put_dialog"):
            yield Label(f"Upload Object to '{self._store_name}'", id="object_put_title")

            # Object name
            yield Label("Object Name:", classes="field_label")
            yield Input(placeholder="my-file.txt", id="object_name")
            yield Label("Name used to identify the object in the store", classes="field_hint")

            yield Label("Description (optional):", classes="field_label")
            yield Input(placeholder="Description of the object", id="object_description")

            # File path input
            yield Label("Load from File:", classes="field_label")
            yield Input(placeholder="/path/to/file.txt", id="file_path")
            yield Button("Load File", variant="default", id="load_file_btn")
            yield Label("", id="file_status")

            yield Label("─── OR ───", classes="or_separator")

            # Manual content input
            yield Label("Enter Content Manually:", classes="field_label")
            yield TextArea(id="object_content")

            with Horizontal(id="button_row"):
                yield Button("Cancel", variant="default", id="cancel_btn")
                yield Button("Upload", variant="primary", id="upload_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "cancel_btn":
            self.dismiss(None)
        elif event.button.id == "load_file_btn":
            self._load_file()
        elif event.button.id == "upload_btn":
            self._upload_object()

    def _load_file(self) -> None:
        """Load file content from the specified path."""
        file_path_str = self.query_one("#file_path", Input).value.strip()
        status_label = self.query_one("#file_status", Label)

        if not file_path_str:
            self.notify("Please enter a file path", severity="warning")
            return

        file_path = Path(file_path_str).expanduser()

        if not file_path.exists():
            self.notify(f"File not found: {file_path}", severity="error")
            status_label.update("[red]File not found[/red]")
            return

        if not file_path.is_file():
            self.notify(f"Not a file: {file_path}", severity="error")
            status_label.update("[red]Not a file[/red]")
            return

        try:
            self._file_data = file_path.read_bytes()
            self._file_name = file_path.name

            # Auto-fill object name if empty
            name_input = self.query_one("#object_name", Input)
            if not name_input.value.strip():
                name_input.value = self._file_name

            # Format size
            size = len(self._file_data)
            if size < 1024:
                size_str = f"{size} B"
            elif size < 1024 * 1024:
                size_str = f"{size / 1024:.1f} KB"
            else:
                size_str = f"{size / (1024 * 1024):.1f} MB"

            status_label.update(f"[green]Loaded: {self._file_name} ({size_str})[/green]")
            self.notify(f"Loaded {self._file_name} ({size_str})")
        except PermissionError:
            self.notify(f"Permission denied: {file_path}", severity="error")
            status_label.update("[red]Permission denied[/red]")
        except Exception as e:
            self.notify(f"Error reading file: {e}", severity="error")
            status_label.update(f"[red]Error: {e}[/red]")

    def _upload_object(self) -> None:
        """Validate and upload object."""
        name = self.query_one("#object_name", Input).value.strip()
        description = self.query_one("#object_description", Input).value.strip()
        content = self.query_one("#object_content", TextArea).text

        if not name:
            self.notify("Object name is required", severity="error")
            return

        # Determine data source
        if self._file_data:
            # Use loaded file data
            data = self._file_data
            from_file = True
        elif content.strip():
            # Use manual content
            data = content.encode("utf-8")
            from_file = False
        else:
            self.notify("Please load a file or enter content", severity="error")
            return

        self.dismiss(
            ObjectPutResult(
                name=name,
                description=description,
                data=data,
                from_file=from_file,
            )
        )

    def action_cancel(self) -> None:
        """Cancel the dialog."""
        self.dismiss(None)
