"""Main NATS TUI application."""

import logging
from datetime import datetime

from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import Footer, Header, Tree

# Set up file logging for debugging
logging.basicConfig(
    filename="/tmp/nats-tui-debug.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

from nats_tui.adapter import ConnectionConfig, NatsAdapter
from nats_tui.app_base import AppBase
from nats_tui.config import ConnectionProfile, NatsTuiConfig
from nats_tui.components import (
    ConnectionDialog,
    ConsumerDetail,
    ConsumerList,
    CreateConsumerDialog,
    CreateConsumerResult,
    CreateStreamDialog,
    CreateStreamResult,
    HelpScreen,
    MessageDetail,
    MessageList,
    PublishDialog,
    PublishResult,
    StatusBar,
    StreamDetail,
    StreamList,
    StreamMessageDetail,
    StreamMessageList,
    SubjectDetails,
    SubjectTree,
    SubscribeDialog,
)
from textual.message import Message

from nats_tui.messages import (
    ConsumerCreated,
    ConsumerDeleted,
    ConsumerError,
    ConsumerInfo,
    ConsumerPaused,
    ConsumersLoaded,
    MessagePublishFailed,
    MessagePublished,
    MessageReceived,
    NatsConnected,
    NatsConnecting,
    NatsConnectionFailed,
    NatsDisconnected,
    ReceivedMessage,
    StreamCreated,
    StreamDeleted,
    StreamError,
    StreamInfo,
    StreamMessageDeleted,
    StreamMessageInfo,
    StreamMessagesLoaded,
    StreamPurged,
    StreamsLoaded,
    SubjectDiscovered,
    SubscriptionStarted,
    SubscriptionStopped,
)


class NatsTuiApp(AppBase):
    """The TUI for NATS cluster management."""

    CSS_PATH = ["global.tcss", "app.tcss"]

    BINDINGS = [
        ("c", "connect", "Connect"),
        ("d", "disconnect", "Disconnect"),
        ("s", "subscribe", "Subscribe"),
        ("u", "unsubscribe", "Unsubscribe"),
        ("p", "publish", "Publish"),
        ("r", "refresh_subjects", "Refresh"),
        ("x", "clear_subjects", "Clear"),
        ("j", "jetstream", "JetStream"),
        ("m", "view_messages", "Messages"),
        ("n", "new_item", "New"),
        Binding("delete", "delete_item", "Delete", priority=True),
        ("P", "purge_stream", "Purge"),
        ("space", "toggle_pause", "Pause/Resume"),
        ("enter", "view_consumers", "Consumers"),
        ("escape", "go_back", "Back"),
        ("q", "quit", "Quit"),
        Binding("question_mark", "show_help", "Help", priority=True),
        Binding("shift+slash", "show_help", "Help", priority=True),
        Binding("f1", "show_help", "Help", priority=True),
    ]
    TITLE = "NATS TUI"

    def __init__(
        self,
        theme: str = "nats-tui",
        server_url: str | None = None,
        config: NatsTuiConfig | None = None,
        profile_data: ConnectionProfile | None = None,
        tls_config: dict | None = None,
    ) -> None:
        super().__init__(theme=theme)
        self._initial_server_url = server_url
        self._config = config or NatsTuiConfig()
        self._profile_data = profile_data
        self._tls_config = tls_config or {}
        self._adapter: NatsAdapter | None = None
        self._subscribed_subject: str | None = None
        self._in_jetstream_view: bool = False
        self._in_consumer_view: bool = False
        self._in_stream_messages_view: bool = False
        self._selected_stream: StreamInfo | None = None
        self._selected_consumer: ConsumerInfo | None = None
        self._selected_stream_message: StreamMessageInfo | None = None
        # Pagination state for stream messages
        self._msg_page_size: int = 15
        self._msg_page_start_seq: int | None = None  # Start seq of current page
        self._msg_first_seq: int = 0  # Stream's first sequence
        self._msg_last_seq: int = 0  # Stream's last sequence
        self._msg_total_count: int = 0  # Total messages in stream

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        logger.debug("compose() START")
        yield Header()
        yield StatusBar()
        logger.debug("compose() yielded Header and StatusBar")
        # Subject browser (default view)
        with Container(id="subject_browser"):
            with Container(id="subject_tree_container"):
                yield SubjectTree()
            with Container(id="subject_details_container"):
                yield SubjectDetails()
        # Message viewer (shown when subscribed)
        with Container(id="message_viewer"):
            with Container(id="message_list_container"):
                yield MessageList()
            with Container(id="message_detail_container"):
                yield MessageDetail()
        # JetStream view (shown when 'j' pressed)
        with Container(id="jetstream_view"):
            with Container(id="stream_list_container"):
                yield StreamList()
            with Container(id="stream_detail_container"):
                yield StreamDetail()
        # Consumer view (shown when Enter on stream)
        with Container(id="consumer_view"):
            with Container(id="consumer_list_container"):
                yield ConsumerList()
            with Container(id="consumer_detail_container"):
                yield ConsumerDetail()
        # Stream messages view (shown when 'm' pressed on stream)
        logger.debug("compose() creating stream_messages_view")
        with Container(id="stream_messages_view"):
            with Container(id="stream_message_list_container"):
                yield StreamMessageList()
            with Container(id="stream_message_detail_container"):
                yield StreamMessageDetail()
        logger.debug("compose() yielding Footer")
        yield Footer()
        logger.debug("compose() END")

    def on_mount(self) -> None:
        """Handle app mount - auto-connect if server_url provided."""
        if self._initial_server_url:
            # Use CLI credentials first, then fall back to profile credentials
            username = self._tls_config.get("username")
            password = self._tls_config.get("password")
            if self._profile_data:
                if not username:
                    username = self._profile_data.get("username")
                if not password:
                    password = self._profile_data.get("password")
            config = ConnectionConfig(
                server_url=self._initial_server_url,
                username=username,
                password=password,
                tls_enabled=self._tls_config.get("tls_enabled", False),
                tls_ca_cert=self._tls_config.get("tls_ca_cert"),
                tls_cert=self._tls_config.get("tls_cert"),
                tls_key=self._tls_config.get("tls_key"),
                tls_insecure=self._tls_config.get("tls_insecure", False),
            )
            self._do_connect(config)

    def action_connect(self) -> None:
        """Show connection dialog."""
        self.push_screen(
            ConnectionDialog(config=self._config, tls_config=self._tls_config),
            self._handle_connection_result,
        )

    def action_disconnect(self) -> None:
        """Disconnect from NATS server."""
        if self._adapter and self._adapter.is_connected:
            self._do_disconnect()
        else:
            self.notify("Not connected", severity="warning")

    async def action_quit(self) -> None:
        """Quit the application, cleaning up connections first."""
        # Cancel any pending workers to avoid hangs
        self.workers.cancel_all()

        # Disconnect cleanly before quitting
        if self._adapter:
            try:
                if self._adapter.is_connected:
                    await self._adapter.disconnect()
            except Exception:
                pass  # Ignore errors during shutdown
            self._adapter = None

        # Force exit
        self.exit()

    def action_show_help(self) -> None:
        """Show help screen."""
        # Cancel any running workers to prevent interference with modal
        if self._in_stream_messages_view:
            self.workers.cancel_group(self, "stream_messages")
        elif self._in_consumer_view:
            self.workers.cancel_group(self, "consumers")
        elif self._in_jetstream_view:
            self.workers.cancel_group(self, "jetstream")
        self.push_screen(HelpScreen())

    def _handle_connection_result(self, result) -> None:
        """Handle result from connection dialog."""
        if result is not None:
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
            self._do_connect(config)

    @work(exclusive=True, group="nats_connect")
    async def _do_connect(self, config: ConnectionConfig) -> None:
        """Connect to NATS in background worker.

        Note: Must use thread=False (default) so that the NATS client is created
        in the main event loop, allowing subsequent operations to use it.
        """
        self.post_message(NatsConnecting(server_url=config.server_url))
        self._adapter = NatsAdapter(config)
        try:
            await self._adapter.connect()
            self.post_message(
                NatsConnected(
                    server_url=config.server_url,
                    server_info=self._adapter.server_info or {},
                )
            )
        except Exception as e:
            self._adapter = None
            self.post_message(
                NatsConnectionFailed(
                    server_url=config.server_url,
                    error=e,
                )
            )

    @work(exclusive=True, group="nats_disconnect")
    async def _do_disconnect(self) -> None:
        """Disconnect from NATS in background worker."""
        if self._adapter:
            await self._adapter.disconnect()
            self._adapter = None
        self.post_message(NatsDisconnected())

    def on_nats_connecting(self, message: NatsConnecting) -> None:
        """Handle connecting state."""
        status_bar = self.query_one(StatusBar)
        status_bar.set_connecting(message.server_url)
        self.notify(f"Connecting to {message.server_url}...")

    def on_nats_connected(self, message: NatsConnected) -> None:
        """Handle connected state."""
        status_bar = self.query_one(StatusBar)
        status_bar.set_connected(message.server_url)
        self.notify(f"Connected to {message.server_url}", severity="information")
        # Start subject discovery
        self._start_discovery()

    def on_nats_connection_failed(self, message: NatsConnectionFailed) -> None:
        """Handle connection failure."""
        status_bar = self.query_one(StatusBar)
        status_bar.set_disconnected()
        self.notify(f"Connection failed: {message.error}", severity="error")

    def on_nats_disconnected(self, message: NatsDisconnected) -> None:
        """Handle disconnected state."""
        status_bar = self.query_one(StatusBar)
        status_bar.set_disconnected()
        # Clear subscription state
        self._subscribed_subject = None
        # Switch back to subject browser if in message view
        self.query_one("#message_viewer").add_class("hidden")
        self.query_one("#subject_browser").remove_class("hidden")
        # Clear the subject tree on disconnect
        tree = self.query_one(SubjectTree)
        tree.clear_subjects()
        details = self.query_one(SubjectDetails)
        details.subject = None
        # Clear messages
        msg_list = self.query_one(MessageList)
        msg_list.clear_messages()
        msg_detail = self.query_one(MessageDetail)
        msg_detail.message = None
        self.notify("Disconnected from NATS", severity="information")

    @work(exclusive=True, group="discovery")
    async def _start_discovery(self) -> None:
        """Start discovering subjects via wildcard subscription."""
        if self._adapter and self._adapter.is_connected:
            async def on_message(subject: str, data: bytes) -> None:
                self.post_message(SubjectDiscovered(subject=subject, data=data))

            await self._adapter.subscribe(">", callback=on_message)
            self.notify("Subject discovery started", severity="information")

    def on_subject_discovered(self, message: SubjectDiscovered) -> None:
        """Handle discovered subject."""
        tree = self.query_one(SubjectTree)
        tree.add_subject(message.subject)

    def on_subject_tree_subject_selected(
        self, message: SubjectTree.SubjectSelected
    ) -> None:
        """Handle subject selection in tree (Enter key)."""
        details = self.query_one(SubjectDetails)
        details.subject = message.node

    def on_tree_node_highlighted(self, message: Tree.NodeHighlighted) -> None:
        """Handle tree node highlight (arrow key navigation)."""
        # Only handle if it's from the SubjectTree
        if not isinstance(message.node.tree, SubjectTree):
            return
        # Update details when navigating
        if message.node.data:
            details = self.query_one(SubjectDetails)
            details.subject = message.node.data

    def action_refresh_subjects(self) -> None:
        """Refresh current view (subjects, streams, consumers, or messages)."""
        if not self._adapter or not self._adapter.is_connected:
            self.notify("Not connected", severity="warning")
            return

        # Context-aware refresh
        if self._in_stream_messages_view:
            # Refresh stream messages
            if self._selected_stream:
                self._load_stream_messages(self._selected_stream.name)
                self.notify("Refreshing messages...")
        elif self._in_consumer_view:
            # Refresh consumers
            if self._selected_stream:
                self._load_consumers(self._selected_stream.name)
                self.notify("Refreshing consumers...")
        elif self._in_jetstream_view:
            # Refresh streams
            self._load_streams()
            self.notify("Refreshing streams...")
        else:
            # Refresh subject discovery
            tree = self.query_one(SubjectTree)
            tree.clear_subjects()
            self._start_discovery()
            self.notify("Refreshing subjects...")

    def action_clear_subjects(self) -> None:
        """Clear all discovered subjects."""
        tree = self.query_one(SubjectTree)
        tree.clear_subjects()
        details = self.query_one(SubjectDetails)
        details.subject = None
        self.notify("Subjects cleared")

    def action_publish(self) -> None:
        """Open publish dialog (or go to newer messages in stream messages view)."""
        # In stream messages view, 'p' navigates to newer (previous) messages
        if self._in_stream_messages_view:
            self.action_prev_page()
            return

        if not self._adapter or not self._adapter.is_connected:
            self.notify("Not connected", severity="warning")
            return

        # Get selected subject if any
        tree = self.query_one(SubjectTree)
        initial_subject = ""
        if tree.selected_subject:
            initial_subject = tree.selected_subject.full_subject

        self.push_screen(
            PublishDialog(initial_subject=initial_subject),
            self._handle_publish_result,
        )

    def _handle_publish_result(self, result: PublishResult | None) -> None:
        """Handle result from publish dialog."""
        if result:
            self._do_publish(result)

    @work(exclusive=True, group="publish")
    async def _do_publish(self, result: PublishResult) -> None:
        """Publish message in background worker."""
        try:
            await self._adapter.publish(
                result.subject,
                result.payload,
                result.headers,
            )
            self.post_message(MessagePublished(subject=result.subject))
        except Exception as e:
            self.post_message(
                MessagePublishFailed(
                    subject=result.subject,
                    error=str(e),
                )
            )

    def on_message_published(self, message: MessagePublished) -> None:
        """Handle successful publish."""
        self.notify(f"Published to {message.subject}", severity="information")

    def on_message_publish_failed(self, message: MessagePublishFailed) -> None:
        """Handle publish failure."""
        self.notify(f"Publish failed: {message.error}", severity="error")

    def action_subscribe(self) -> None:
        """Open subscribe dialog."""
        if not self._adapter or not self._adapter.is_connected:
            self.notify("Not connected", severity="warning")
            return

        if self._subscribed_subject:
            self.notify(
                f"Already subscribed to {self._subscribed_subject}. "
                "Press 'u' to unsubscribe first.",
                severity="warning",
            )
            return

        # Get selected subject if any
        tree = self.query_one(SubjectTree)
        initial_subject = ""
        if tree.selected_subject:
            initial_subject = tree.selected_subject.full_subject

        self.push_screen(
            SubscribeDialog(initial_subject=initial_subject),
            self._handle_subscribe_result,
        )

    def _handle_subscribe_result(self, subject: str | None) -> None:
        """Handle result from subscribe dialog."""
        if subject:
            self._start_subscription(subject)

    @work(exclusive=True, group="subscription")
    async def _start_subscription(self, subject: str) -> None:
        """Start subscription in background worker."""
        if not self._adapter:
            return

        # Unsubscribe from discovery first
        await self._adapter.unsubscribe_all()

        async def on_message(subj: str, data: bytes) -> None:
            msg = ReceivedMessage(
                subject=subj,
                payload=data,
                timestamp=datetime.now(),
                size=len(data),
            )
            self.post_message(MessageReceived(received_message=msg))

        await self._adapter.subscribe(subject, callback=on_message)
        self._subscribed_subject = subject
        self.post_message(SubscriptionStarted(subject=subject))

    def on_subscription_started(self, message: SubscriptionStarted) -> None:
        """Handle subscription started."""
        # Switch to message view
        self.query_one("#subject_browser").add_class("hidden")
        self.query_one("#message_viewer").remove_class("hidden")
        self.query_one("#message_viewer").add_class("active")
        # Clear previous messages
        msg_list = self.query_one(MessageList)
        msg_list.clear_messages()
        msg_detail = self.query_one(MessageDetail)
        msg_detail.message = None
        self.notify(f"Subscribed to {message.subject}", severity="information")

    def on_message_received(self, message: MessageReceived) -> None:
        """Handle received message."""
        msg_list = self.query_one(MessageList)
        msg_list.add_message(message.received_message)

    def on_message_list_message_selected(
        self, message: MessageList.MessageSelected
    ) -> None:
        """Handle message selection in list."""
        msg_detail = self.query_one(MessageDetail)
        msg_detail.message = message.message

    def action_unsubscribe(self) -> None:
        """Unsubscribe from current subject."""
        if not self._subscribed_subject:
            self.notify("Not subscribed", severity="warning")
            return

        self._stop_subscription()

    @work(exclusive=True, group="subscription")
    async def _stop_subscription(self) -> None:
        """Stop subscription in background worker."""
        if self._adapter:
            await self._adapter.unsubscribe_all()

        self._subscribed_subject = None
        self.post_message(SubscriptionStopped())

        # Restart discovery
        if self._adapter and self._adapter.is_connected:
            async def on_message(subject: str, data: bytes) -> None:
                self.post_message(SubjectDiscovered(subject=subject, data=data))

            await self._adapter.subscribe(">", callback=on_message)

    def on_subscription_stopped(self, message: SubscriptionStopped) -> None:
        """Handle subscription stopped."""
        # Switch back to subject browser
        self.query_one("#message_viewer").remove_class("active")
        self.query_one("#message_viewer").add_class("hidden")
        self.query_one("#subject_browser").remove_class("hidden")
        self.notify("Unsubscribed", severity="information")

    # JetStream Actions

    def action_jetstream(self) -> None:
        """Switch to JetStream view."""
        if not self._adapter or not self._adapter.is_connected:
            self.notify("Not connected", severity="warning")
            return

        # If in stream messages view, go back to JetStream stream list
        if self._in_stream_messages_view:
            # Cancel any running stream_messages workers first
            self.workers.cancel_group(self, "stream_messages")
            self.query_one("#stream_messages_view").remove_class("active")
            self.query_one("#stream_messages_view").add_class("hidden")
            self._in_stream_messages_view = False
            self._selected_stream_message = None
            # Clear message detail
            msg_detail = self.query_one(StreamMessageDetail)
            msg_detail.message = None
            # Show JetStream view and set focus
            self.query_one("#jetstream_view").remove_class("hidden")
            self.query_one("#jetstream_view").add_class("active")
            self._in_jetstream_view = True
            # Focus the stream list
            self.query_one(StreamList).focus()
            return

        # If in consumer view, go back to JetStream stream list
        if self._in_consumer_view:
            # Cancel any running consumer workers first
            self.workers.cancel_group(self, "consumers")
            self.query_one("#consumer_view").remove_class("active")
            self.query_one("#consumer_view").add_class("hidden")
            self._in_consumer_view = False
            self._selected_consumer = None
            # Clear consumer detail
            consumer_detail = self.query_one(ConsumerDetail)
            consumer_detail.consumer = None
            # Show JetStream view and set focus
            self.query_one("#jetstream_view").remove_class("hidden")
            self.query_one("#jetstream_view").add_class("active")
            self._in_jetstream_view = True
            # Focus the stream list
            self.query_one(StreamList).focus()
            return

        # Coming from subject browser - hide it, show JetStream
        self.query_one("#subject_browser").add_class("hidden")
        self.query_one("#message_viewer").add_class("hidden")
        self.query_one("#message_viewer").remove_class("active")
        self.query_one("#jetstream_view").remove_class("hidden")
        self.query_one("#jetstream_view").add_class("active")
        self._in_jetstream_view = True

        # Focus the stream list
        self.query_one(StreamList).focus()

        # Load streams
        self._load_streams()

    def action_go_back(self) -> None:
        """Go back to previous view."""
        if self._in_stream_messages_view:
            # Cancel any running stream_messages workers
            self.workers.cancel_group(self, "stream_messages")
            # Go back from stream messages view to stream view
            self.query_one("#stream_messages_view").remove_class("active")
            self.query_one("#stream_messages_view").add_class("hidden")
            self.query_one("#jetstream_view").remove_class("hidden")
            self.query_one("#jetstream_view").add_class("active")
            self._in_stream_messages_view = False
            self._selected_stream_message = None
            # Clear message detail
            msg_detail = self.query_one(StreamMessageDetail)
            msg_detail.message = None
            # Focus the stream list
            self.query_one(StreamList).focus()
        elif self._in_consumer_view:
            # Cancel any running consumer workers
            self.workers.cancel_group(self, "consumers")
            # Go back from consumer view to stream view
            self.query_one("#consumer_view").remove_class("active")
            self.query_one("#consumer_view").add_class("hidden")
            self.query_one("#jetstream_view").remove_class("hidden")
            self.query_one("#jetstream_view").add_class("active")
            self._in_consumer_view = False
            self._selected_consumer = None
            # Clear consumer detail
            consumer_detail = self.query_one(ConsumerDetail)
            consumer_detail.consumer = None
            # Focus the stream list
            self.query_one(StreamList).focus()
        elif self._in_jetstream_view:
            # Cancel any running jetstream workers
            self.workers.cancel_group(self, "jetstream")
            # Go back from stream view to subject browser
            self.query_one("#jetstream_view").remove_class("active")
            self.query_one("#jetstream_view").add_class("hidden")
            self.query_one("#subject_browser").remove_class("hidden")
            self._in_jetstream_view = False
            self._selected_stream = None
            # Focus the subject tree
            self.query_one(SubjectTree).focus()

    @work(exclusive=True, group="jetstream")
    async def _load_streams(self) -> None:
        """Load streams in background.

        Note: Must use thread=False (default) because nats-py client is bound to
        the main event loop. Using thread=True causes the async code to run in a
        different thread's event loop, which breaks asyncio objects.
        """
        if not self._adapter:
            self.post_message(StreamError(error="Not connected"))
            return

        try:
            streams_info = await self._adapter.list_streams()
            streams = [self._convert_stream_info(s) for s in streams_info]
            self.post_message(StreamsLoaded(streams=streams))
        except Exception as e:
            self.post_message(StreamError(error=f"Failed to load streams: {e}"))

    def _convert_stream_info(self, info) -> StreamInfo:
        """Convert nats.js StreamInfo to our StreamInfo."""
        config = info.config
        state = info.state

        # Get storage type string
        storage = "file"
        if hasattr(config, "storage"):
            storage = str(config.storage).lower().replace("storagetype.", "")

        # Get retention type string
        retention = "limits"
        if hasattr(config, "retention"):
            retention = str(config.retention).lower().replace("retentionpolicy.", "")

        return StreamInfo(
            name=config.name,
            subjects=list(config.subjects) if config.subjects else [],
            messages=state.messages,
            bytes=state.bytes,
            storage=storage,
            retention=retention,
            consumers=state.consumer_count,
            first_seq=state.first_seq,
            last_seq=state.last_seq,
            max_msgs=config.max_msgs if config.max_msgs else -1,
            max_bytes=config.max_bytes if config.max_bytes else -1,
            max_age=config.max_age if config.max_age else 0,
        )

    def on_streams_loaded(self, message: StreamsLoaded) -> None:
        """Handle streams loaded."""
        stream_list = self.query_one(StreamList)
        stream_list.set_streams(message.streams)
        if not message.streams:
            self.notify("No streams found. Press 'n' to create one.")
        elif message.streams:
            # Auto-select the first stream
            self._selected_stream = message.streams[0]
            stream_detail = self.query_one(StreamDetail)
            stream_detail.stream = message.streams[0]

    def on_stream_list_stream_selected(
        self, message: StreamList.StreamSelected
    ) -> None:
        """Handle stream selection in list - show cached then fetch fresh."""
        # Show cached info immediately
        self._selected_stream = message.stream
        stream_detail = self.query_one(StreamDetail)
        stream_detail.stream = message.stream
        # Then fetch fresh stream info for accurate stats
        self._refresh_selected_stream_info(message.stream.name)

    @work(exclusive=True, group="stream_info")
    async def _refresh_selected_stream_info(self, stream_name: str) -> None:
        """Fetch fresh stream info for the selected stream."""
        if not self._adapter:
            return

        try:
            info = await self._adapter.get_stream_info(stream_name)
            if info:
                fresh_stream = self._convert_stream_info(info)
                self._selected_stream = fresh_stream
                stream_detail = self.query_one(StreamDetail)
                stream_detail.stream = fresh_stream
        except Exception:
            pass  # Keep showing cached info

    def action_new_item(self) -> None:
        """Open create dialog for stream or consumer (or go to older messages)."""
        # In stream messages view, 'n' navigates to older (next) messages
        if self._in_stream_messages_view:
            self.action_next_page()
            return

        if not self._adapter or not self._adapter.is_connected:
            self.notify("Not connected", severity="warning")
            return

        if self._in_consumer_view and self._selected_stream:
            # Create consumer
            self.push_screen(
                CreateConsumerDialog(self._selected_stream.name),
                self._handle_create_consumer_result,
            )
        elif self._in_jetstream_view:
            # Create stream
            self.push_screen(CreateStreamDialog(), self._handle_create_stream_result)
        else:
            self.notify("Press 'j' to enter JetStream view first", severity="warning")

    def _handle_create_stream_result(self, result: CreateStreamResult | None) -> None:
        """Handle result from create stream dialog."""
        if result:
            self._do_create_stream(result)

    @work(exclusive=True, group="jetstream")
    async def _do_create_stream(self, result: CreateStreamResult) -> None:
        """Create stream in background."""
        if not self._adapter:
            return

        try:
            await self._adapter.create_stream(
                name=result.name,
                subjects=result.subjects,
                storage=result.storage,
                retention=result.retention,
                discard=result.discard,
                max_msgs=result.max_msgs,
                max_bytes=result.max_bytes,
                max_age=result.max_age,
                max_msg_size=result.max_msg_size,
                max_msgs_per_subject=result.max_msgs_per_subject,
                num_replicas=result.num_replicas,
                duplicate_window=result.duplicate_window,
                allow_rollup=result.allow_rollup,
                deny_delete=result.deny_delete,
                deny_purge=result.deny_purge,
            )
            self.post_message(StreamCreated(name=result.name))
        except Exception as e:
            self.post_message(StreamError(error=str(e)))

    def on_stream_created(self, message: StreamCreated) -> None:
        """Handle stream created."""
        self.notify(f"Stream '{message.name}' created", severity="information")
        # Reload streams
        self._load_streams()

    def on_stream_error(self, message: StreamError) -> None:
        """Handle stream error."""
        self.notify(f"Stream error: {message.error}", severity="error")

    def action_delete_item(self) -> None:
        """Delete the selected stream, consumer, or message."""
        logger.debug("action_delete_item called")
        logger.debug(f"  _in_stream_messages_view={self._in_stream_messages_view}")
        logger.debug(f"  _in_consumer_view={self._in_consumer_view}")
        logger.debug(f"  _in_jetstream_view={self._in_jetstream_view}")

        if self._in_stream_messages_view:
            logger.debug("In stream_messages_view branch")

            # Get the selected stream info
            stream_name = self._selected_stream.name if self._selected_stream else None
            if not stream_name:
                self.notify("No stream context", severity="warning")
                return

            # Get the currently highlighted message from the list
            try:
                msg_list = self.query_one(StreamMessageList)
                selected_msg = msg_list.selected_message
            except Exception as e:
                logger.exception(f"Error getting message: {e}")
                self.notify(f"Error getting message: {e}", severity="error")
                return

            if not selected_msg:
                self.notify("No message selected", severity="warning")
                return

            # Delete directly without confirmation
            msg_seq = selected_msg.seq
            logger.debug(f"Deleting message: seq={msg_seq}")
            self._do_delete_message(stream_name, msg_seq)
            return
        elif self._in_consumer_view:
            # Cancel any running consumer workers first
            self.workers.cancel_group(self, "consumers")
            # Get the currently highlighted consumer from the list
            consumer_list = self.query_one(ConsumerList)
            selected_consumer = consumer_list.selected_consumer
            if not selected_consumer or not self._selected_stream:
                self.notify("No consumer selected", severity="warning")
                return
            # Delete directly without confirmation
            self._do_delete_consumer(
                self._selected_stream.name,
                selected_consumer.name,
            )
        elif self._in_jetstream_view:
            # Cancel any running jetstream workers first
            self.workers.cancel_group(self, "jetstream")
            # Get the currently highlighted stream from the list
            stream_list = self.query_one(StreamList)
            selected_stream = stream_list.selected_stream
            if not selected_stream:
                self.notify("No stream selected", severity="warning")
                return
            # Delete directly without confirmation
            self._do_delete_stream(selected_stream.name)

    @work(exclusive=True, group="jetstream")
    async def _do_delete_stream(self, name: str) -> None:
        """Delete stream in background."""
        if not self._adapter:
            return

        success = await self._adapter.delete_stream(name)
        if success:
            self.post_message(StreamDeleted(name=name))
        else:
            self.post_message(StreamError(error=f"Failed to delete stream '{name}'"))

    def on_stream_deleted(self, message: StreamDeleted) -> None:
        """Handle stream deleted."""
        self.notify(f"Stream '{message.name}' deleted", severity="information")
        self._selected_stream = None
        # Clear detail view
        stream_detail = self.query_one(StreamDetail)
        stream_detail.stream = None
        # Reload streams
        self._load_streams()

    def action_purge_stream(self) -> None:
        """Purge the selected stream directly."""
        # Allow purge from both JetStream view and stream messages view
        if not self._in_jetstream_view and not self._in_stream_messages_view:
            return

        if not self._selected_stream:
            self.notify("No stream selected", severity="warning")
            return

        # Cancel any running workers first
        if self._in_stream_messages_view:
            self.workers.cancel_group(self, "stream_messages")
        self.workers.cancel_group(self, "jetstream")

        stream_name = self._selected_stream.name
        msg_count = self._selected_stream.messages

        # Purge directly without confirmation
        self._do_purge_stream(stream_name, msg_count)

    @work(exclusive=True, group="jetstream")
    async def _do_purge_stream(self, name: str, msg_count: int) -> None:
        """Purge stream in background."""
        if not self._adapter:
            return

        success = await self._adapter.purge_stream(name)
        if success:
            self.post_message(StreamPurged(name=name, messages_removed=msg_count))
        else:
            self.post_message(StreamError(error=f"Failed to purge stream '{name}'"))

    def on_stream_purged(self, message: StreamPurged) -> None:
        """Handle stream purged."""
        self.notify(
            f"Purged {message.messages_removed:,} messages from '{message.name}'",
            severity="information",
        )
        # Reload streams to show updated state
        self._load_streams()
        # If in stream messages view, reload messages (will be empty)
        if self._in_stream_messages_view and self._selected_stream:
            self._load_stream_messages(self._selected_stream.name)

    # Message Deletion

    @work(exclusive=True, group="stream_messages")
    async def _do_delete_message(self, stream_name: str, seq: int) -> None:
        """Delete a message from stream in background."""
        if not self._adapter:
            return

        success = await self._adapter.delete_message(stream_name, seq)
        if success:
            self.post_message(StreamMessageDeleted(stream_name=stream_name, seq=seq))
        else:
            self.notify(f"Failed to delete message #{seq}", severity="error")

    def on_stream_message_deleted(self, message: StreamMessageDeleted) -> None:
        """Handle stream message deleted."""
        self.notify(
            f"Deleted message #{message.seq} from '{message.stream_name}'",
            severity="information",
        )
        # Clear selection
        self._selected_stream_message = None
        msg_detail = self.query_one(StreamMessageDetail)
        msg_detail.message = None
        # Reload messages
        self._load_stream_messages(message.stream_name)
        # Reload streams to update message count
        self._load_streams()

    # Consumer Actions

    def action_view_consumers(self) -> None:
        """View consumers for selected stream."""
        if not self._in_jetstream_view or self._in_consumer_view:
            return

        if not self._selected_stream:
            self.notify("Select a stream first", severity="warning")
            return

        # Switch to consumer view
        self.query_one("#jetstream_view").remove_class("active")
        self.query_one("#jetstream_view").add_class("hidden")
        self.query_one("#consumer_view").remove_class("hidden")
        self.query_one("#consumer_view").add_class("active")
        self._in_consumer_view = True

        # Focus the consumer list
        self.query_one(ConsumerList).focus()

        # Load consumers
        self._load_consumers(self._selected_stream.name)

    @work(exclusive=True, group="consumers")
    async def _load_consumers(self, stream_name: str) -> None:
        """Load consumers in background."""
        if not self._adapter:
            return

        consumers_info = await self._adapter.list_consumers(stream_name)
        consumers = [self._convert_consumer_info(stream_name, c) for c in consumers_info]
        self.post_message(ConsumersLoaded(stream_name=stream_name, consumers=consumers))

    def _convert_consumer_info(self, stream_name: str, info) -> ConsumerInfo:
        """Convert nats.js ConsumerInfo to our ConsumerInfo."""
        config = info.config

        # Get policy strings
        deliver_policy = "all"
        if hasattr(config, "deliver_policy"):
            deliver_policy = str(config.deliver_policy).lower().replace("deliverpolicy.", "")

        ack_policy = "explicit"
        if hasattr(config, "ack_policy"):
            ack_policy = str(config.ack_policy).lower().replace("ackpolicy.", "")

        return ConsumerInfo(
            name=config.name or config.durable_name or "unknown",
            stream_name=stream_name,
            durable_name=config.durable_name,
            deliver_policy=deliver_policy,
            ack_policy=ack_policy,
            filter_subject=config.filter_subject,
            num_pending=info.num_pending or 0,
            num_waiting=info.num_waiting or 0,
            num_ack_pending=info.num_ack_pending or 0,
            num_redelivered=info.num_redelivered or 0,
            max_deliver=config.max_deliver or -1,
            paused=getattr(info, "paused", False) or False,
        )

    def on_consumers_loaded(self, message: ConsumersLoaded) -> None:
        """Handle consumers loaded."""
        consumer_list = self.query_one(ConsumerList)
        consumer_list.set_consumers(message.stream_name, message.consumers)
        if not message.consumers:
            self.notify("No consumers found. Press 'n' to create one.")
        elif message.consumers:
            # Auto-select the first consumer
            self._selected_consumer = message.consumers[0]
            consumer_detail = self.query_one(ConsumerDetail)
            consumer_detail.consumer = message.consumers[0]

    def on_consumer_list_consumer_selected(
        self, message: ConsumerList.ConsumerSelected
    ) -> None:
        """Handle consumer selection in list."""
        self._selected_consumer = message.consumer
        consumer_detail = self.query_one(ConsumerDetail)
        consumer_detail.consumer = message.consumer

    def _handle_create_consumer_result(
        self, result: CreateConsumerResult | None
    ) -> None:
        """Handle result from create consumer dialog."""
        if result and self._selected_stream:
            self._do_create_consumer(self._selected_stream.name, result)

    @work(exclusive=True, group="consumers")
    async def _do_create_consumer(
        self, stream_name: str, result: CreateConsumerResult
    ) -> None:
        """Create consumer in background."""
        if not self._adapter:
            return

        try:
            await self._adapter.create_consumer(
                stream=stream_name,
                name=result.name,
                durable_name=result.durable_name,
                deliver_policy=result.deliver_policy,
                ack_policy=result.ack_policy,
                filter_subject=result.filter_subject,
            )
            self.post_message(
                ConsumerCreated(stream_name=stream_name, consumer_name=result.name)
            )
        except Exception as e:
            self.post_message(ConsumerError(error=str(e)))

    def on_consumer_created(self, message: ConsumerCreated) -> None:
        """Handle consumer created."""
        self.notify(
            f"Consumer '{message.consumer_name}' created", severity="information"
        )
        # Reload consumers
        self._load_consumers(message.stream_name)

    def on_consumer_error(self, message: ConsumerError) -> None:
        """Handle consumer error."""
        self.notify(f"Consumer error: {message.error}", severity="error")

    @work(exclusive=True, group="consumers")
    async def _do_delete_consumer(self, stream_name: str, consumer_name: str) -> None:
        """Delete consumer in background."""
        if not self._adapter:
            return

        success = await self._adapter.delete_consumer(stream_name, consumer_name)
        if success:
            self.post_message(
                ConsumerDeleted(stream_name=stream_name, consumer_name=consumer_name)
            )
        else:
            self.post_message(
                ConsumerError(error=f"Failed to delete consumer '{consumer_name}'")
            )

    def on_consumer_deleted(self, message: ConsumerDeleted) -> None:
        """Handle consumer deleted."""
        self.notify(
            f"Consumer '{message.consumer_name}' deleted", severity="information"
        )
        self._selected_consumer = None
        # Clear detail view
        consumer_detail = self.query_one(ConsumerDetail)
        consumer_detail.consumer = None
        # Reload consumers
        self._load_consumers(message.stream_name)

    def action_toggle_pause(self) -> None:
        """Toggle pause/resume for selected consumer."""
        if not self._in_consumer_view:
            return

        if not self._selected_consumer or not self._selected_stream:
            self.notify("No consumer selected", severity="warning")
            return

        stream_name = self._selected_stream.name
        consumer_name = self._selected_consumer.name
        is_paused = self._selected_consumer.paused

        if is_paused:
            self._do_resume_consumer(stream_name, consumer_name)
        else:
            self._do_pause_consumer(stream_name, consumer_name)

    @work(exclusive=True, group="consumers")
    async def _do_pause_consumer(self, stream_name: str, consumer_name: str) -> None:
        """Pause consumer in background."""
        if not self._adapter:
            return

        success = await self._adapter.pause_consumer(stream_name, consumer_name)
        if success:
            self.post_message(
                ConsumerPaused(
                    stream_name=stream_name, consumer_name=consumer_name, paused=True
                )
            )
        else:
            self.post_message(
                ConsumerError(error=f"Failed to pause consumer '{consumer_name}'")
            )

    @work(exclusive=True, group="consumers")
    async def _do_resume_consumer(self, stream_name: str, consumer_name: str) -> None:
        """Resume consumer in background."""
        if not self._adapter:
            return

        success = await self._adapter.resume_consumer(stream_name, consumer_name)
        if success:
            self.post_message(
                ConsumerPaused(
                    stream_name=stream_name, consumer_name=consumer_name, paused=False
                )
            )
        else:
            self.post_message(
                ConsumerError(error=f"Failed to resume consumer '{consumer_name}'")
            )

    def on_consumer_paused(self, message: ConsumerPaused) -> None:
        """Handle consumer pause state changed."""
        action = "paused" if message.paused else "resumed"
        self.notify(
            f"Consumer '{message.consumer_name}' {action}", severity="information"
        )
        # Reload consumers to show updated state
        self._load_consumers(message.stream_name)

    # Stream Message Browsing Actions

    def action_view_messages(self) -> None:
        """View messages in the selected stream."""
        if not self._in_jetstream_view or self._in_consumer_view:
            self.notify(
                "Press 'j' for JetStream view, select a stream, then press 'm'",
                severity="warning",
            )
            return

        if not self._selected_stream:
            self.notify("Select a stream first", severity="warning")
            return

        if self._selected_stream.messages == 0:
            self.notify("Stream has no messages", severity="warning")
            return

        # Switch to stream messages view
        self.query_one("#jetstream_view").remove_class("active")
        self.query_one("#jetstream_view").add_class("hidden")
        self.query_one("#stream_messages_view").remove_class("hidden")
        self.query_one("#stream_messages_view").add_class("active")
        self._in_stream_messages_view = True
        self._in_jetstream_view = False  # Fix state inconsistency

        # Focus the message list
        self.query_one(StreamMessageList).focus()

        # Load messages
        self._load_stream_messages(self._selected_stream.name)

    @work(exclusive=True, group="stream_messages")
    async def _load_stream_messages(
        self, stream_name: str, start_seq: int | None = None
    ) -> None:
        """Load messages from a stream in background with pagination.

        Args:
            stream_name: Name of the stream
            start_seq: Starting sequence number (None = start from last/newest)
        """
        if not self._adapter:
            return

        try:
            raw_messages, first_seq, last_seq, total_count = (
                await self._adapter.get_stream_messages(
                    stream_name, count=self._msg_page_size, start_seq=start_seq
                )
            )
            messages = [self._convert_raw_message(m) for m in raw_messages]

            # Determine actual page start sequence
            page_start = start_seq if start_seq is not None else last_seq

            self.post_message(
                StreamMessagesLoaded(
                    stream_name=stream_name,
                    messages=messages,
                    first_seq=first_seq,
                    last_seq=last_seq,
                    total_count=total_count,
                    page_start_seq=page_start,
                )
            )
        except Exception as e:
            self.notify(f"Failed to load messages: {e}", severity="error")

    def _convert_raw_message(self, raw_msg) -> StreamMessageInfo:
        """Convert nats.js RawStreamMsg to our StreamMessageInfo."""
        return StreamMessageInfo(
            seq=raw_msg.seq if raw_msg.seq else 0,
            subject=raw_msg.subject if raw_msg.subject else "",
            data=raw_msg.data,
            time=raw_msg.time if hasattr(raw_msg, "time") else None,
            headers=dict(raw_msg.headers) if raw_msg.headers else None,
        )

    def on_stream_messages_loaded(self, message: StreamMessagesLoaded) -> None:
        """Handle stream messages loaded."""
        # Store pagination state
        self._msg_first_seq = message.first_seq
        self._msg_last_seq = message.last_seq
        self._msg_total_count = message.total_count
        self._msg_page_start_seq = message.page_start_seq

        msg_list = self.query_one(StreamMessageList)
        msg_list.set_messages(
            message.stream_name,
            message.messages,
            first_seq=message.first_seq,
            last_seq=message.last_seq,
            total_count=message.total_count,
            page_start_seq=message.page_start_seq,
        )
        if not message.messages:
            self.notify("No messages found in stream")
        elif message.messages:
            # Show the first message in the detail view
            msg_detail = self.query_one(StreamMessageDetail)
            msg_detail.message = message.messages[0]

    def on_stream_message_list_message_selected(
        self, message: StreamMessageList.MessageSelected
    ) -> None:
        """Handle message selection in stream message list."""
        self._selected_stream_message = message.message
        msg_detail = self.query_one(StreamMessageDetail)
        msg_detail.message = message.message

    def action_next_page(self) -> None:
        """Go to older messages (lower sequence numbers)."""
        if not self._in_stream_messages_view:
            return
        if not self._selected_stream:
            return

        # Calculate next page start (older = lower sequence)
        if self._msg_page_start_seq is None:
            return

        # Get the lowest seq in current page and go further back
        msg_list = self.query_one(StreamMessageList)
        if msg_list._messages:
            current_min_seq = min(m.seq for m in msg_list._messages)
            # Go to next page (older messages)
            next_start = current_min_seq - 1
            if next_start >= self._msg_first_seq:
                self._load_stream_messages(
                    self._selected_stream.name, start_seq=next_start
                )
            else:
                self.notify("Already at oldest messages", severity="warning")
        else:
            self.notify("No messages to paginate", severity="warning")

    def action_prev_page(self) -> None:
        """Go to newer messages (higher sequence numbers)."""
        if not self._in_stream_messages_view:
            return
        if not self._selected_stream:
            return

        # Calculate previous page start (newer = higher sequence)
        if self._msg_page_start_seq is None:
            return

        # Get the highest seq in current page and go forward
        msg_list = self.query_one(StreamMessageList)
        if msg_list._messages:
            current_max_seq = max(m.seq for m in msg_list._messages)
            # Go to previous page (newer messages)
            prev_start = current_max_seq + self._msg_page_size
            if prev_start <= self._msg_last_seq:
                self._load_stream_messages(
                    self._selected_stream.name, start_seq=prev_start
                )
            elif current_max_seq < self._msg_last_seq:
                # Not at the newest yet, go to newest
                self._load_stream_messages(self._selected_stream.name, start_seq=None)
            else:
                self.notify("Already at newest messages", severity="warning")
        else:
            self.notify("No messages to paginate", severity="warning")
