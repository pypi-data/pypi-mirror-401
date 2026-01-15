"""Subject details panel for NATS TUI."""

from datetime import datetime

from textual.reactive import reactive
from textual.widgets import Static

from nats_tui.components.subject_tree import SubjectNode


class SubjectDetails(Static):
    """Panel showing details of the selected subject."""

    DEFAULT_CSS = """
    SubjectDetails {
        width: 1fr;
        height: 1fr;
        border: round $primary;
        background: $surface;
        padding: 1 2;
    }
    """

    subject: reactive[SubjectNode | None] = reactive(None)

    def render(self) -> str:
        """Render the subject details."""
        if not self.subject:
            return (
                "No subject selected\n\n"
                "Select a subject from the tree\n"
                "to view its details."
            )

        last_seen = "Never"
        if self.subject.last_seen:
            delta = datetime.now() - self.subject.last_seen
            seconds = int(delta.total_seconds())
            if seconds < 60:
                last_seen = f"{seconds}s ago"
            elif seconds < 3600:
                last_seen = f"{seconds // 60}m ago"
            else:
                last_seen = f"{seconds // 3600}h ago"

        return (
            f"Subject: {self.subject.full_subject}\n"
            f"Messages: {self.subject.message_count}\n"
            f"Last seen: {last_seen}\n\n"
            "Future actions:\n"
            "  's' - Subscribe to this subject\n"
            "  'p' - Publish to this subject"
        )
