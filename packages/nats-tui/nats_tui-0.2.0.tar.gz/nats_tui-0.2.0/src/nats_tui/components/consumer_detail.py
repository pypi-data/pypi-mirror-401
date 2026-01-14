"""Consumer detail widget for displaying consumer information."""

from textual.reactive import reactive
from textual.widgets import Static

from nats_tui.messages import ConsumerInfo


class ConsumerDetail(Static):
    """Display consumer details."""

    consumer: reactive[ConsumerInfo | None] = reactive(None)

    def render(self) -> str:
        """Render consumer details."""
        if not self.consumer:
            return (
                "Select a consumer to view details...\n\n"
                "Press 'n' to create a new consumer."
            )

        c = self.consumer

        # Paused status
        paused_status = "[bold red]PAUSED[/bold red]" if c.paused else "[green]Active[/green]"

        # Filter subject display
        filter_display = c.filter_subject if c.filter_subject else "(all subjects)"

        return (
            f"[bold]{c.name}[/bold]\n"
            f"Status: {paused_status}\n\n"
            f"[dim]Configuration[/dim]\n"
            f"  Stream: {c.stream_name}\n"
            f"  Durable: {c.durable_name or 'N/A'}\n"
            f"  Deliver Policy: {c.deliver_policy}\n"
            f"  Ack Policy: {c.ack_policy}\n"
            f"  Filter Subject: {filter_display}\n"
            f"  Max Deliver: {c.max_deliver if c.max_deliver > 0 else 'unlimited'}\n\n"
            f"[dim]State[/dim]\n"
            f"  Pending: {c.num_pending:,}\n"
            f"  Waiting: {c.num_waiting:,}\n"
            f"  Ack Pending: {c.num_ack_pending:,}\n"
            f"  Redelivered: {c.num_redelivered:,}\n\n"
            f"[dim]Actions[/dim]\n"
            f"  Space: {'Resume' if c.paused else 'Pause'}\n"
            f"  Delete: press 'Delete' key"
        )
