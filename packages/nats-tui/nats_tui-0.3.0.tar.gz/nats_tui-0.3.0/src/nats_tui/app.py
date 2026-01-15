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
    CreateKVDialog,
    CreateKVResult,
    CreateObjectStoreDialog,
    CreateObjectStoreResult,
    CreateStreamDialog,
    CreateStreamResult,
    HelpScreen,
    KVBucketList,
    KVKeyList,
    KVPutDialog,
    KVPutResult,
    KVValueDetail,
    MessageDetail,
    MessageList,
    ObjectDetail,
    ObjectList,
    ObjectPutDialog,
    ObjectPutResult,
    ObjectStoreList,
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
    KVBucketCreated,
    KVBucketDeleted,
    KVBucketInfo,
    KVBucketsLoaded,
    KVEntry,
    KVEntryLoaded,
    KVError,
    KVKeyDeleted,
    KVKeysLoaded,
    KVValuePut,
    MessagePublishFailed,
    MessagePublished,
    MessageReceived,
    NatsConnected,
    NatsConnecting,
    NatsConnectionFailed,
    NatsDisconnected,
    ObjectDeleted,
    ObjectError,
    ObjectInfo,
    ObjectInfoLoaded,
    ObjectsLoaded,
    ObjectStoreCreated,
    ObjectStoreDeleted,
    ObjectStoreInfo,
    ObjectStoresLoaded,
    ObjectUploaded,
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
        ("k", "kv_view", "Key/Value"),
        ("o", "object_store_view", "Object Store"),
        ("m", "view_messages", "Messages"),
        ("n", "new_item", "New"),
        Binding("delete", "delete_item", "Delete", priority=True),
        ("P", "purge_stream", "Purge"),
        ("e", "edit_kv", "Edit"),
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
        # Key/Value state
        self._in_kv_view: bool = False
        self._selected_kv_bucket: KVBucketInfo | None = None
        self._selected_kv_key: str | None = None
        # KV key pagination state
        self._kv_key_page_size: int = 50
        self._kv_key_offset: int = 0
        self._kv_key_total: int = 0
        # Object Store state
        self._in_object_store_view: bool = False
        self._selected_object_store: ObjectStoreInfo | None = None
        self._selected_object: str | None = None
        # Object pagination state
        self._object_page_size: int = 50
        self._object_offset: int = 0
        self._object_total: int = 0

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
        # Key/Value view (shown when 'k' pressed)
        logger.debug("compose() creating kv_view")
        with Container(id="kv_view"):
            with Container(id="kv_bucket_list_container"):
                yield KVBucketList()
            with Container(id="kv_key_list_container"):
                yield KVKeyList()
            with Container(id="kv_value_detail_container"):
                yield KVValueDetail()
        # Object Store view (shown when 'o' pressed)
        logger.debug("compose() creating object_store_view")
        with Container(id="object_store_view"):
            with Container(id="object_store_list_container"):
                yield ObjectStoreList()
            with Container(id="object_list_container"):
                yield ObjectList()
            with Container(id="object_detail_container"):
                yield ObjectDetail()
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
        if self._in_object_store_view:
            self.workers.cancel_group(self, "object_store")
            self.workers.cancel_group(self, "objects")
            self.workers.cancel_group(self, "object_info")
        elif self._in_kv_view:
            self.workers.cancel_group(self, "kv")
            self.workers.cancel_group(self, "kv_keys")
            self.workers.cancel_group(self, "kv_entry")
        elif self._in_stream_messages_view:
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
        """Refresh current view (subjects, streams, consumers, messages, KV, or Object Store)."""
        if not self._adapter or not self._adapter.is_connected:
            self.notify("Not connected", severity="warning")
            return

        # Context-aware refresh
        if self._in_object_store_view:
            # Refresh Object Stores and objects
            self._load_object_stores()
            self.notify("Refreshing Object Stores...")
        elif self._in_kv_view:
            # Refresh KV buckets and keys
            self._load_kv_buckets()
            self.notify("Refreshing KV buckets...")
        elif self._in_stream_messages_view:
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
        """Open publish dialog (or go to newer messages in stream messages view, or prev page in KV view)."""
        # In stream messages view, 'p' navigates to newer (previous) messages
        if self._in_stream_messages_view:
            self.action_prev_page()
            return

        # In KV view with key list focus, 'p' navigates to previous page
        if self._in_kv_view:
            try:
                key_list = self.query_one(KVKeyList)
                if key_list.has_focus and key_list.has_prev_page:
                    self._kv_keys_prev_page()
                    return
            except Exception:
                pass

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
        if self._in_object_store_view:
            # Cancel any running object store workers
            self.workers.cancel_group(self, "object_store")
            self.workers.cancel_group(self, "objects")
            self.workers.cancel_group(self, "object_info")
            # Go back from Object Store view to subject browser
            self.query_one("#object_store_view").remove_class("active")
            self.query_one("#object_store_view").add_class("hidden")
            self.query_one("#subject_browser").remove_class("hidden")
            self._in_object_store_view = False
            self._selected_object_store = None
            self._selected_object = None
            # Focus the subject tree
            self.query_one(SubjectTree).focus()
        elif self._in_kv_view:
            # Cancel any running kv workers
            self.workers.cancel_group(self, "kv")
            self.workers.cancel_group(self, "kv_keys")
            self.workers.cancel_group(self, "kv_entry")
            # Go back from KV view to subject browser
            self.query_one("#kv_view").remove_class("active")
            self.query_one("#kv_view").add_class("hidden")
            self.query_one("#subject_browser").remove_class("hidden")
            self._in_kv_view = False
            self._selected_kv_bucket = None
            self._selected_kv_key = None
            # Focus the subject tree
            self.query_one(SubjectTree).focus()
        elif self._in_stream_messages_view:
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
        """Open create dialog for stream, consumer, KV bucket, or Object Store (or go to older messages)."""
        logger.debug(f"action_new_item called, _in_kv_view={self._in_kv_view}, _in_object_store_view={self._in_object_store_view}")
        # In stream messages view, 'n' navigates to older (next) messages
        if self._in_stream_messages_view:
            self.action_next_page()
            return

        if not self._adapter or not self._adapter.is_connected:
            self.notify("Not connected", severity="warning")
            return

        if self._in_object_store_view:
            # Context-aware: check which panel has focus
            # If store list has focus -> create store
            # If object list has focus -> next page (if paginated) or upload object
            try:
                store_list = self.query_one(ObjectStoreList)
                object_list = self.query_one(ObjectList)

                if store_list.has_focus:
                    logger.debug("Store list has focus - creating new store")
                    self.push_screen(CreateObjectStoreDialog(), self._handle_create_object_store_result)
                elif object_list.has_focus and self._selected_object_store:
                    # If paginated and has next page, navigate
                    if object_list.has_next_page:
                        logger.debug("Object list has focus - navigating to next page")
                        self._objects_next_page()
                    else:
                        logger.debug("Object list has focus - uploading new object")
                        self._open_object_put_dialog()
                elif self._selected_object_store:
                    # Default: if a store is selected, upload an object
                    logger.debug("Default: uploading new object to existing store")
                    self._open_object_put_dialog()
                else:
                    logger.debug("No store selected - creating new store")
                    self.push_screen(CreateObjectStoreDialog(), self._handle_create_object_store_result)
            except Exception as e:
                logger.exception(f"Error determining focus: {e}")
                # Fallback to old behavior
                if self._selected_object_store:
                    self._open_object_put_dialog()
                else:
                    self.push_screen(CreateObjectStoreDialog(), self._handle_create_object_store_result)
        elif self._in_kv_view:
            # Context-aware: check which panel has focus
            # If bucket list has focus -> create bucket
            # If key list has focus -> next page (if paginated) or create key
            try:
                bucket_list = self.query_one(KVBucketList)
                key_list = self.query_one(KVKeyList)

                if bucket_list.has_focus:
                    logger.debug("Bucket list has focus - creating new bucket")
                    self.push_screen(CreateKVDialog(), self._handle_create_kv_result)
                elif key_list.has_focus and self._selected_kv_bucket:
                    # If paginated and has next page, navigate
                    if key_list.has_next_page:
                        logger.debug("Key list has focus - navigating to next page")
                        self._kv_keys_next_page()
                    else:
                        logger.debug("Key list has focus - creating new key")
                        self._open_kv_put_dialog()
                elif self._selected_kv_bucket:
                    # Default: if a bucket is selected, create a key
                    logger.debug("Default: creating new key in existing bucket")
                    self._open_kv_put_dialog()
                else:
                    logger.debug("No bucket selected - creating new bucket")
                    self.push_screen(CreateKVDialog(), self._handle_create_kv_result)
            except Exception as e:
                logger.exception(f"Error determining focus: {e}")
                # Fallback to old behavior
                if self._selected_kv_bucket:
                    self._open_kv_put_dialog()
                else:
                    self.push_screen(CreateKVDialog(), self._handle_create_kv_result)
        elif self._in_consumer_view and self._selected_stream:
            # Create consumer
            self.push_screen(
                CreateConsumerDialog(self._selected_stream.name),
                self._handle_create_consumer_result,
            )
        elif self._in_jetstream_view:
            # Create stream
            self.push_screen(CreateStreamDialog(), self._handle_create_stream_result)
        else:
            self.notify("Press 'j' for JetStream or 'k' for Key/Value view", severity="warning")

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
        """Delete the selected stream, consumer, message, KV bucket, key, Object Store, or object."""
        logger.debug("action_delete_item called")
        logger.debug(f"  _in_stream_messages_view={self._in_stream_messages_view}")
        logger.debug(f"  _in_consumer_view={self._in_consumer_view}")
        logger.debug(f"  _in_jetstream_view={self._in_jetstream_view}")
        logger.debug(f"  _in_kv_view={self._in_kv_view}")
        logger.debug(f"  _in_object_store_view={self._in_object_store_view}")

        if self._in_object_store_view:
            # Delete Object or Object Store
            if self._selected_object and self._selected_object_store:
                # Delete object
                self._do_delete_object(
                    self._selected_object_store.name, self._selected_object
                )
            elif self._selected_object_store:
                # Delete store
                self._do_delete_object_store(self._selected_object_store.name)
            else:
                self.notify("No store or object selected", severity="warning")
            return
        elif self._in_kv_view:
            # Delete KV key or bucket
            if self._selected_kv_key and self._selected_kv_bucket:
                # Delete key
                self._do_delete_kv_key(
                    self._selected_kv_bucket.name, self._selected_kv_key
                )
            elif self._selected_kv_bucket:
                # Delete bucket
                self._do_delete_kv_bucket(self._selected_kv_bucket.name)
            else:
                self.notify("No bucket or key selected", severity="warning")
            return
        elif self._in_stream_messages_view:
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

    # Key/Value Store Actions

    def action_kv_view(self) -> None:
        """Switch to Key/Value store view."""
        logger.debug("action_kv_view called")
        if not self._adapter or not self._adapter.is_connected:
            logger.debug("action_kv_view: not connected")
            self.notify("Not connected", severity="warning")
            return

        # If already in KV view, do nothing
        if self._in_kv_view:
            logger.debug("action_kv_view: already in kv view")
            return

        logger.debug("action_kv_view: showing kv view")
        # Hide all other views and show KV view
        self.query_one("#subject_browser").add_class("hidden")
        self.query_one("#message_viewer").add_class("hidden")
        self.query_one("#message_viewer").remove_class("active")
        self.query_one("#jetstream_view").add_class("hidden")
        self.query_one("#jetstream_view").remove_class("active")
        self.query_one("#consumer_view").add_class("hidden")
        self.query_one("#consumer_view").remove_class("active")
        self.query_one("#stream_messages_view").add_class("hidden")
        self.query_one("#stream_messages_view").remove_class("active")
        self.query_one("#kv_view").remove_class("hidden")
        self.query_one("#kv_view").add_class("active")

        self._in_kv_view = True
        self._in_jetstream_view = False
        self._in_consumer_view = False
        self._in_stream_messages_view = False

        # Focus the bucket list
        self.query_one(KVBucketList).focus()

        # Load KV buckets
        self._load_kv_buckets()

    @work(exclusive=True, group="kv")
    async def _load_kv_buckets(self) -> None:
        """Load KV buckets in background."""
        logger.debug("_load_kv_buckets called")
        if not self._adapter:
            logger.debug("_load_kv_buckets: no adapter")
            self.post_message(KVError(error="Not connected"))
            return

        try:
            logger.debug("Calling adapter.list_kv_buckets()")
            buckets_data = await self._adapter.list_kv_buckets()
            logger.debug(f"Got {len(buckets_data)} buckets from adapter")
            buckets = []
            logger.debug(f"Starting loop through {len(buckets_data)} buckets")
            for name, kv in buckets_data:
                logger.debug(f"Processing bucket: {name}, kv object: {kv}")
                try:
                    # Use the kv object we already have to get status
                    logger.debug(f"Getting status for bucket: {name}")
                    status = await kv.status()
                    logger.debug(f"Got status for {name}: {status}")

                    # Get actual key count by calling keys()
                    # status.values includes tombstones, so we need the real count
                    try:
                        actual_keys = await kv.keys()
                        key_count = len(actual_keys)
                        logger.debug(f"Got actual key count for {name}: {key_count}")
                    except Exception:
                        # Fallback to status.values if keys() fails
                        key_count = status.values if hasattr(status, "values") else 0
                        logger.debug(f"Using status.values for {name}: {key_count}")

                    bucket_info = KVBucketInfo(
                        name=name,
                        values=key_count,
                        history=status.history if hasattr(status, "history") else 1,
                        ttl=status.ttl if hasattr(status, "ttl") else 0,
                        max_bytes=(
                            status.max_bytes if hasattr(status, "max_bytes") else -1
                        ),
                        storage=(
                            str(status.storage).lower().replace("storagetype.", "")
                            if hasattr(status, "storage")
                            else "file"
                        ),
                    )
                    logger.debug(f"Created KVBucketInfo for {name}: {bucket_info}")
                    buckets.append(bucket_info)
                except Exception as e:
                    logger.exception(f"Exception getting status for {name}: {e}")
                    # If we can't get status, add with defaults
                    buckets.append(
                        KVBucketInfo(
                            name=name,
                            values=0,
                            history=1,
                            ttl=0,
                            max_bytes=-1,
                            storage="file",
                        )
                    )
            logger.debug(f"Loop complete. Have {len(buckets)} buckets to display")
            # Directly update the UI instead of using message system
            # This works around potential message routing issues in workers
            msg = KVBucketsLoaded(buckets=buckets)
            self.call_later(lambda m=msg: self._handle_kv_buckets_loaded(m))
            logger.debug("Scheduled _handle_kv_buckets_loaded via call_later")
        except Exception as e:
            logger.exception(f"Exception in _load_kv_buckets: {e}")
            self.post_message(KVError(error=f"Failed to load KV buckets: {e}"))

    def _handle_kv_buckets_loaded(self, message: KVBucketsLoaded) -> None:
        """Handle KV buckets loaded."""
        logger.debug(f"_handle_kv_buckets_loaded: {len(message.buckets)} buckets")
        bucket_list = self.query_one(KVBucketList)
        bucket_list.set_buckets(message.buckets)
        if not message.buckets:
            self.notify("No KV buckets found. Press 'n' to create one.")
            # Clear key list and value detail
            key_list = self.query_one(KVKeyList)
            key_list.set_keys("", [])
            value_detail = self.query_one(KVValueDetail)
            value_detail.entry = None
        elif message.buckets:
            # Auto-select the first bucket
            self._selected_kv_bucket = message.buckets[0]
            self._kv_key_offset = 0  # Reset pagination
            self._load_kv_keys(message.buckets[0].name, offset=0)

    def on_kv_bucket_list_bucket_selected(
        self, message: KVBucketList.BucketSelected
    ) -> None:
        """Handle bucket selection in list."""
        logger.debug(f"on_kv_bucket_list_bucket_selected: bucket={message.bucket.name}")
        self._handle_kv_bucket_selection(message.bucket)

    def _handle_kv_bucket_selection(self, bucket: KVBucketInfo) -> None:
        """Handle bucket selection - load keys for the bucket."""
        logger.debug(f"_handle_kv_bucket_selection: bucket={bucket.name}")
        self._selected_kv_bucket = bucket
        self._selected_kv_key = None
        # Reset pagination when switching buckets
        self._kv_key_offset = 0
        # Clear value detail when bucket changes
        value_detail = self.query_one(KVValueDetail)
        value_detail.entry = None
        # Load keys for selected bucket (first page)
        self._load_kv_keys(bucket.name, offset=0)

    @work(exclusive=True, group="kv_keys")
    async def _load_kv_keys(self, bucket_name: str, offset: int = 0) -> None:
        """Load keys for a bucket in background with pagination."""
        logger.debug(f"_load_kv_keys called: bucket={bucket_name}, offset={offset}")
        if not self._adapter:
            logger.debug("_load_kv_keys: no adapter")
            return

        try:
            keys, total_count = await self._adapter.kv_keys(
                bucket_name, offset=offset, limit=self._kv_key_page_size
            )
            logger.debug(f"Got {len(keys)} keys for bucket {bucket_name} (total: {total_count})")
            msg = KVKeysLoaded(
                bucket=bucket_name,
                keys=keys,
                total_count=total_count,
                offset=offset,
                limit=self._kv_key_page_size,
            )
            self.call_later(lambda m=msg: self._handle_kv_keys_loaded(m))
        except Exception as e:
            logger.exception(f"Failed to load keys: {e}")
            self.call_later(lambda err=str(e): self.notify(f"Failed to load keys: {err}", severity="error"))

    def _handle_kv_keys_loaded(self, message: KVKeysLoaded) -> None:
        """Handle KV keys loaded."""
        logger.debug(
            f"_handle_kv_keys_loaded: bucket={message.bucket}, keys={len(message.keys)}, "
            f"total={message.total_count}, offset={message.offset}"
        )
        # Update pagination state
        self._kv_key_offset = message.offset
        self._kv_key_total = message.total_count

        key_list = self.query_one(KVKeyList)
        key_list.set_keys(
            message.bucket,
            message.keys,
            total_count=message.total_count,
            offset=message.offset,
            limit=message.limit,
        )
        if message.keys:
            # Auto-select the first key and load its value
            self._selected_kv_key = message.keys[0]
            self._load_kv_entry(message.bucket, message.keys[0])
        else:
            # Clear value detail
            value_detail = self.query_one(KVValueDetail)
            value_detail.entry = None

    def _kv_keys_next_page(self) -> None:
        """Navigate to next page of KV keys."""
        if not self._selected_kv_bucket:
            return
        new_offset = self._kv_key_offset + self._kv_key_page_size
        if new_offset < self._kv_key_total:
            logger.debug(f"KV keys next page: offset {self._kv_key_offset} -> {new_offset}")
            self._load_kv_keys(self._selected_kv_bucket.name, offset=new_offset)

    def _kv_keys_prev_page(self) -> None:
        """Navigate to previous page of KV keys."""
        if not self._selected_kv_bucket:
            return
        new_offset = max(0, self._kv_key_offset - self._kv_key_page_size)
        if new_offset != self._kv_key_offset:
            logger.debug(f"KV keys prev page: offset {self._kv_key_offset} -> {new_offset}")
            self._load_kv_keys(self._selected_kv_bucket.name, offset=new_offset)

    def on_kv_key_list_key_selected(self, message: KVKeyList.KeySelected) -> None:
        """Handle key selection in list."""
        logger.debug(f"on_kv_key_list_key_selected: key={message.key}")
        self._handle_kv_key_selection(message.key)

    def on_list_view_highlighted(self, message) -> None:
        """Handle ListView highlight events for KV bucket/key and Object Store/object navigation."""
        # Handle KV view
        if self._in_kv_view:
            try:
                bucket_list = self.query_one(KVBucketList)
                key_list = self.query_one(KVKeyList)

                # Check if the sender is the KVBucketList
                if message._sender is bucket_list:
                    # Use selected_bucket property to get the actual current selection
                    # This avoids stale event item references after list refresh
                    bucket = bucket_list.selected_bucket
                    if bucket:
                        logger.debug(f"on_list_view_highlighted (KVBucketList): bucket={bucket.name}")
                        self._handle_kv_bucket_selection(bucket)
                    return

                # Check if the sender is the KVKeyList
                if message._sender is key_list:
                    # Use selected_key property to get the actual current selection
                    # This avoids stale event item references after list refresh
                    key = key_list.selected_key
                    if key:
                        logger.debug(f"on_list_view_highlighted (KVKeyList): key={key}")
                        self._handle_kv_key_selection(key)
                    return
            except Exception as e:
                logger.exception(f"Error in on_list_view_highlighted (KV): {e}")

        # Handle Object Store view
        if self._in_object_store_view:
            try:
                store_list = self.query_one(ObjectStoreList)
                object_list = self.query_one(ObjectList)

                # Check if the sender is the ObjectStoreList
                if message._sender is store_list:
                    # Use selected_store property to get the actual current selection
                    # This avoids stale event item references after list refresh
                    store = store_list.selected_store
                    if store:
                        logger.debug(f"on_list_view_highlighted (ObjectStoreList): store={store.name}")
                        self._handle_object_store_selection(store)
                    return

                # Check if the sender is the ObjectList
                if message._sender is object_list:
                    # Use selected_object property to get the actual current selection
                    # This avoids stale event item references after list refresh
                    obj = object_list.selected_object
                    if obj:
                        logger.debug(f"on_list_view_highlighted (ObjectList): object={obj}")
                        self._handle_object_selection(obj)
                    return
            except Exception as e:
                logger.exception(f"Error in on_list_view_highlighted (ObjectStore): {e}")

    def _handle_kv_key_selection(self, key: str) -> None:
        """Handle key selection - load the entry value."""
        logger.debug(f"_handle_kv_key_selection: key={key}")
        self._selected_kv_key = key
        if self._selected_kv_bucket:
            logger.debug(f"Loading entry for bucket={self._selected_kv_bucket.name}, key={key}")
            self._load_kv_entry(self._selected_kv_bucket.name, key)
        else:
            logger.debug("No bucket selected, not loading entry")

    @work(exclusive=True, group="kv_entry")
    async def _load_kv_entry(self, bucket_name: str, key: str) -> None:
        """Load a KV entry in background."""
        logger.debug(f"_load_kv_entry called: bucket={bucket_name}, key={key}")
        if not self._adapter:
            logger.debug("_load_kv_entry: no adapter")
            return

        try:
            entry = await self._adapter.kv_get(bucket_name, key)
            logger.debug(f"Got entry: {entry}")
            if entry:
                kv_entry = KVEntry(
                    bucket=bucket_name,
                    key=key,
                    value=entry.value,
                    revision=entry.revision if hasattr(entry, "revision") else 0,
                    created=entry.created if hasattr(entry, "created") else None,
                    operation=(
                        str(entry.operation).upper().replace("KVOPERATION.", "")
                        if hasattr(entry, "operation")
                        else "PUT"
                    ),
                )
                logger.debug(f"Created KVEntry: {kv_entry}")
                msg = KVEntryLoaded(entry=kv_entry)
                self.call_later(lambda m=msg: self._handle_kv_entry_loaded(m))
            else:
                self.call_later(lambda k=key: self.notify(f"Key '{k}' not found", severity="error"))
        except Exception as e:
            logger.exception(f"Failed to load entry: {e}")
            self.call_later(lambda err=str(e): self.notify(f"Failed to load entry: {err}", severity="error"))

    def _handle_kv_entry_loaded(self, message: KVEntryLoaded) -> None:
        """Handle KV entry loaded."""
        logger.debug(f"_handle_kv_entry_loaded: key={message.entry.key}")
        value_detail = self.query_one(KVValueDetail)
        value_detail.entry = message.entry

    def on_kv_error(self, message: KVError) -> None:
        """Handle KV error."""
        logger.debug(f"on_kv_error: {message.error}")
        self.notify(f"KV error: {message.error}", severity="error")

    def action_edit_kv(self) -> None:
        """Edit the selected KV entry or create new one."""
        if not self._in_kv_view:
            return

        if not self._adapter or not self._adapter.is_connected:
            self.notify("Not connected", severity="warning")
            return

        if not self._selected_kv_bucket:
            self.notify("Select a bucket first", severity="warning")
            return

        # If a key is selected, edit it; otherwise create new
        if self._selected_kv_key:
            # Get current value for editing
            self._open_kv_edit_dialog()
        else:
            # Create new key
            self._open_kv_put_dialog()

    def _open_kv_put_dialog(self) -> None:
        """Open dialog to create a new KV entry."""
        logger.debug(f"_open_kv_put_dialog called, bucket: {self._selected_kv_bucket}")
        if not self._selected_kv_bucket:
            logger.debug("_open_kv_put_dialog: no bucket selected")
            return
        logger.debug(f"Opening KVPutDialog for bucket: {self._selected_kv_bucket.name}")
        self.push_screen(
            KVPutDialog(bucket=self._selected_kv_bucket.name),
            self._handle_kv_put_result,
        )

    def _open_kv_edit_dialog(self) -> None:
        """Open dialog to edit an existing KV entry."""
        if not self._selected_kv_bucket or not self._selected_kv_key:
            return

        # Get current value from the detail view
        value_detail = self.query_one(KVValueDetail)
        current_value = ""
        if value_detail.entry:
            current_value = value_detail.entry.value_str

        self.push_screen(
            KVPutDialog(
                bucket=self._selected_kv_bucket.name,
                key=self._selected_kv_key,
                value=current_value,
                edit_mode=True,
            ),
            self._handle_kv_put_result,
        )

    def _handle_kv_put_result(self, result: KVPutResult | None) -> None:
        """Handle result from KV put dialog."""
        logger.debug(f"_handle_kv_put_result called with: {result}")
        if result and self._selected_kv_bucket:
            logger.debug(f"Calling _do_kv_put for bucket={self._selected_kv_bucket.name}, key={result.key}")
            self._do_kv_put(self._selected_kv_bucket.name, result.key, result.value)
        else:
            logger.debug(f"Not putting: result={result}, bucket={self._selected_kv_bucket}")

    @work(exclusive=True, group="kv")
    async def _do_kv_put(self, bucket_name: str, key: str, value: str) -> None:
        """Put a KV value in background."""
        logger.debug(f"_do_kv_put called: bucket={bucket_name}, key={key}, value_len={len(value)}")
        if not self._adapter:
            logger.debug("_do_kv_put: no adapter")
            return

        try:
            logger.debug(f"Calling adapter.kv_put({bucket_name}, {key})")
            revision = await self._adapter.kv_put(
                bucket_name, key, value.encode("utf-8")
            )
            logger.debug(f"kv_put returned revision: {revision}")
            # Use call_later to handle the result on the main thread
            msg = KVValuePut(bucket=bucket_name, key=key, revision=revision)
            self.call_later(lambda m=msg: self._handle_kv_value_put(m))
        except Exception as e:
            logger.exception(f"Failed to put value: {e}")
            self.call_later(lambda err=str(e): self.notify(f"Failed to put value: {err}", severity="error"))

    def _handle_kv_value_put(self, message: KVValuePut) -> None:
        """Handle KV value put success."""
        logger.debug(f"_handle_kv_value_put: bucket={message.bucket}, key={message.key}, revision={message.revision}")
        self.notify(
            f"Saved '{message.key}' (revision {message.revision})",
            severity="information",
        )
        # Reload keys to show new/updated key
        self._load_kv_keys(message.bucket)
        # Reload buckets to update value count
        self._load_kv_buckets()

    def _handle_create_kv_result(self, result: CreateKVResult | None) -> None:
        """Handle result from create KV bucket dialog."""
        logger.debug(f"_handle_create_kv_result called with: {result}")
        if result:
            self._do_create_kv_bucket(result)

    @work(exclusive=True, group="kv")
    async def _do_create_kv_bucket(self, result: CreateKVResult) -> None:
        """Create a KV bucket in background."""
        logger.debug(f"_do_create_kv_bucket called with: {result.name}")
        if not self._adapter:
            logger.debug("_do_create_kv_bucket: no adapter")
            return

        try:
            logger.debug(f"Creating KV bucket: {result.name}")
            await self._adapter.create_kv_bucket(
                name=result.name,
                history=result.history,
                ttl=result.ttl,
                max_bytes=result.max_bytes,
                storage=result.storage,
            )
            logger.debug(f"KV bucket created successfully: {result.name}")
            self.post_message(KVBucketCreated(name=result.name))
        except Exception as e:
            logger.exception(f"Failed to create KV bucket: {e}")
            self.post_message(KVError(error=f"Failed to create bucket: {e}"))

    def on_kv_bucket_created(self, message: KVBucketCreated) -> None:
        """Handle KV bucket created."""
        logger.debug(f"on_kv_bucket_created: {message.name}")
        self.notify(f"Bucket '{message.name}' created", severity="information")
        # Reload buckets
        self._load_kv_buckets()

    @work(exclusive=True, group="kv")
    async def _do_delete_kv_bucket(self, name: str) -> None:
        """Delete a KV bucket in background."""
        if not self._adapter:
            return

        success = await self._adapter.delete_kv_bucket(name)
        if success:
            msg = KVBucketDeleted(name=name)
            self.call_later(lambda m=msg: self._handle_kv_bucket_deleted(m))
        else:
            self.call_later(
                lambda: self.notify(f"Failed to delete bucket '{name}'", severity="error")
            )

    def on_kv_bucket_deleted(self, message: KVBucketDeleted) -> None:
        """Handle KV bucket deleted (from message routing)."""
        self._handle_kv_bucket_deleted(message)

    def _handle_kv_bucket_deleted(self, message: KVBucketDeleted) -> None:
        """Handle KV bucket deleted."""
        logger.debug(f"_handle_kv_bucket_deleted: name={message.name}")
        self.notify(f"Bucket '{message.name}' deleted", severity="information")
        self._selected_kv_bucket = None
        self._selected_kv_key = None
        self._kv_key_offset = 0  # Reset pagination
        # Clear key list and value detail
        key_list = self.query_one(KVKeyList)
        key_list.set_keys("", [])
        value_detail = self.query_one(KVValueDetail)
        value_detail.entry = None
        # Reload buckets
        self._load_kv_buckets()

    @work(exclusive=True, group="kv")
    async def _do_delete_kv_key(self, bucket_name: str, key: str) -> None:
        """Delete a KV key in background."""
        if not self._adapter:
            return

        success = await self._adapter.kv_delete(bucket_name, key)
        if success:
            msg = KVKeyDeleted(bucket=bucket_name, key=key)
            self.call_later(lambda m=msg: self._handle_kv_key_deleted(m))
        else:
            self.call_later(
                lambda: self.notify(f"Failed to delete key '{key}'", severity="error")
            )

    def on_kv_key_deleted(self, message: KVKeyDeleted) -> None:
        """Handle KV key deleted (from message routing)."""
        self._handle_kv_key_deleted(message)

    def _handle_kv_key_deleted(self, message: KVKeyDeleted) -> None:
        """Handle KV key deleted."""
        logger.debug(f"_handle_kv_key_deleted: bucket={message.bucket}, key={message.key}")
        self.notify(f"Key '{message.key}' deleted", severity="information")
        self._selected_kv_key = None
        # Clear value detail
        value_detail = self.query_one(KVValueDetail)
        value_detail.entry = None
        # Reload keys (with current pagination offset)
        self._load_kv_keys(message.bucket, offset=self._kv_key_offset)
        # Reload buckets to update value count
        self._load_kv_buckets()

    # Object Store Actions

    def action_object_store_view(self) -> None:
        """Switch to Object Store view."""
        logger.debug("action_object_store_view called")
        if not self._adapter or not self._adapter.is_connected:
            logger.debug("action_object_store_view: not connected")
            self.notify("Not connected", severity="warning")
            return

        # If already in Object Store view, do nothing
        if self._in_object_store_view:
            logger.debug("action_object_store_view: already in object store view")
            return

        logger.debug("action_object_store_view: showing object store view")
        # Hide all other views and show Object Store view
        self.query_one("#subject_browser").add_class("hidden")
        self.query_one("#message_viewer").add_class("hidden")
        self.query_one("#message_viewer").remove_class("active")
        self.query_one("#jetstream_view").add_class("hidden")
        self.query_one("#jetstream_view").remove_class("active")
        self.query_one("#consumer_view").add_class("hidden")
        self.query_one("#consumer_view").remove_class("active")
        self.query_one("#stream_messages_view").add_class("hidden")
        self.query_one("#stream_messages_view").remove_class("active")
        self.query_one("#kv_view").add_class("hidden")
        self.query_one("#kv_view").remove_class("active")
        self.query_one("#object_store_view").remove_class("hidden")
        self.query_one("#object_store_view").add_class("active")

        self._in_object_store_view = True
        self._in_kv_view = False
        self._in_jetstream_view = False
        self._in_consumer_view = False
        self._in_stream_messages_view = False

        # Focus the store list
        self.query_one(ObjectStoreList).focus()

        # Load Object Stores
        self._load_object_stores()

    @work(exclusive=True, group="object_store")
    async def _load_object_stores(self) -> None:
        """Load Object Stores in background."""
        logger.debug("_load_object_stores called")
        if not self._adapter:
            logger.debug("_load_object_stores: no adapter")
            self.post_message(ObjectError(error="Not connected"))
            return

        try:
            logger.debug("Calling adapter.list_object_stores()")
            stores_data = await self._adapter.list_object_stores()
            logger.debug(f"Got {len(stores_data)} object stores from adapter")
            stores = []
            for name, obj_store in stores_data:
                logger.debug(f"Processing object store: {name}")
                try:
                    # Get status for the store
                    status = await self._adapter.object_store_status(name)
                    logger.debug(f"Got status for {name}: {status}")

                    # Get actual object count by listing objects
                    try:
                        objects_list, total_count = await self._adapter.list_objects(name, limit=1)
                        object_count = total_count
                        logger.debug(f"Got actual object count for {name}: {object_count}")
                    except Exception:
                        object_count = 0
                        logger.debug(f"Using 0 for object count for {name}")

                    store_info = ObjectStoreInfo(
                        name=name,
                        description=status.description if hasattr(status, "description") else "",
                        objects=object_count,
                        size=status.size if hasattr(status, "size") else 0,
                        storage=(
                            str(status.storage).lower().replace("storagetype.", "")
                            if hasattr(status, "storage")
                            else "file"
                        ),
                        replicas=status.replicas if hasattr(status, "replicas") else 1,
                        ttl=status.ttl if hasattr(status, "ttl") else 0,
                        max_bytes=status.max_bytes if hasattr(status, "max_bytes") else -1,
                    )
                    logger.debug(f"Created ObjectStoreInfo for {name}: {store_info}")
                    stores.append(store_info)
                except Exception as e:
                    logger.exception(f"Exception getting status for {name}: {e}")
                    # Add with defaults if we can't get status
                    stores.append(
                        ObjectStoreInfo(
                            name=name,
                            description="",
                            objects=0,
                            size=0,
                            storage="file",
                            replicas=1,
                            ttl=0,
                            max_bytes=-1,
                        )
                    )
            logger.debug(f"Loop complete. Have {len(stores)} stores to display")
            # Use call_later to handle the result on the main thread
            msg = ObjectStoresLoaded(stores=stores)
            self.call_later(lambda m=msg: self._handle_object_stores_loaded(m))
            logger.debug("Scheduled _handle_object_stores_loaded via call_later")
        except Exception as e:
            logger.exception(f"Exception in _load_object_stores: {e}")
            self.post_message(ObjectError(error=f"Failed to load Object Stores: {e}"))

    def _handle_object_stores_loaded(self, message: ObjectStoresLoaded) -> None:
        """Handle Object Stores loaded."""
        logger.debug(f"_handle_object_stores_loaded: {len(message.stores)} stores")
        store_list = self.query_one(ObjectStoreList)
        store_list.set_stores(message.stores)
        if not message.stores:
            self.notify("No Object Stores found. Press 'n' to create one.")
            # Clear object list and detail
            object_list = self.query_one(ObjectList)
            object_list.set_objects("", [])
            object_detail = self.query_one(ObjectDetail)
            object_detail.object_info = None
        elif message.stores:
            # Auto-select the first store
            self._selected_object_store = message.stores[0]
            self._object_offset = 0  # Reset pagination
            self._load_objects(message.stores[0].name, offset=0)

    def on_object_store_list_store_selected(
        self, message: ObjectStoreList.StoreSelected
    ) -> None:
        """Handle store selection in list."""
        logger.debug(f"on_object_store_list_store_selected: store={message.store.name}")
        self._handle_object_store_selection(message.store)

    def _handle_object_store_selection(self, store: ObjectStoreInfo) -> None:
        """Handle store selection - load objects for the store."""
        logger.debug(f"_handle_object_store_selection: store={store.name}")
        self._selected_object_store = store
        self._selected_object = None
        # Reset pagination when switching stores
        self._object_offset = 0
        # Clear object detail when store changes
        object_detail = self.query_one(ObjectDetail)
        object_detail.object_info = None
        # Load objects for selected store (first page)
        self._load_objects(store.name, offset=0)

    @work(exclusive=True, group="objects")
    async def _load_objects(self, store_name: str, offset: int = 0) -> None:
        """Load objects for a store in background with pagination."""
        logger.debug(f"_load_objects called: store={store_name}, offset={offset}")
        if not self._adapter:
            logger.debug("_load_objects: no adapter")
            return

        try:
            objects, total_count = await self._adapter.list_objects(
                store_name, offset=offset, limit=self._object_page_size
            )
            logger.debug(f"Got {len(objects)} objects for store {store_name} (total: {total_count})")

            # Convert to ObjectInfo
            object_infos = []
            for obj in objects:
                obj_info = ObjectInfo(
                    store=store_name,
                    name=obj.name if hasattr(obj, "name") else str(obj),
                    size=obj.size if hasattr(obj, "size") else 0,
                    chunks=obj.chunks if hasattr(obj, "chunks") else 0,
                    modified=obj.mtime if hasattr(obj, "mtime") else None,
                    digest=obj.digest if hasattr(obj, "digest") else None,
                    deleted=obj.deleted if hasattr(obj, "deleted") else False,
                )
                object_infos.append(obj_info)

            msg = ObjectsLoaded(
                store=store_name,
                objects=object_infos,
                total_count=total_count,
                offset=offset,
                limit=self._object_page_size,
            )
            self.call_later(lambda m=msg: self._handle_objects_loaded(m))
        except Exception as e:
            logger.exception(f"Failed to load objects: {e}")
            self.call_later(lambda err=str(e): self.notify(f"Failed to load objects: {err}", severity="error"))

    def _handle_objects_loaded(self, message: ObjectsLoaded) -> None:
        """Handle objects loaded."""
        logger.debug(
            f"_handle_objects_loaded: store={message.store}, objects={len(message.objects)}, "
            f"total={message.total_count}, offset={message.offset}"
        )
        # Update pagination state
        self._object_offset = message.offset
        self._object_total = message.total_count

        object_list = self.query_one(ObjectList)
        object_list.set_objects(
            message.store,
            message.objects,
            total_count=message.total_count,
            offset=message.offset,
            limit=message.limit,
        )
        if message.objects:
            # Auto-select the first object and load its info
            self._selected_object = message.objects[0].name
            self._load_object_info(message.store, message.objects[0].name)
        else:
            # Clear object detail
            object_detail = self.query_one(ObjectDetail)
            object_detail.object_info = None

    def _objects_next_page(self) -> None:
        """Navigate to next page of objects."""
        if not self._selected_object_store:
            return
        new_offset = self._object_offset + self._object_page_size
        if new_offset < self._object_total:
            logger.debug(f"Objects next page: offset {self._object_offset} -> {new_offset}")
            self._load_objects(self._selected_object_store.name, offset=new_offset)

    def _objects_prev_page(self) -> None:
        """Navigate to previous page of objects."""
        if not self._selected_object_store:
            return
        new_offset = max(0, self._object_offset - self._object_page_size)
        if new_offset != self._object_offset:
            logger.debug(f"Objects prev page: offset {self._object_offset} -> {new_offset}")
            self._load_objects(self._selected_object_store.name, offset=new_offset)

    def on_object_list_object_selected(self, message: ObjectList.ObjectSelected) -> None:
        """Handle object selection in list."""
        logger.debug(f"on_object_list_object_selected: object={message.name}")
        self._handle_object_selection(message.name)

    def _handle_object_selection(self, name: str) -> None:
        """Handle object selection - load the object info."""
        logger.debug(f"_handle_object_selection: name={name}")
        self._selected_object = name
        if self._selected_object_store:
            logger.debug(f"Loading info for store={self._selected_object_store.name}, object={name}")
            self._load_object_info(self._selected_object_store.name, name)
        else:
            logger.debug("No store selected, not loading object info")

    @work(exclusive=True, group="object_info")
    async def _load_object_info(self, store_name: str, name: str) -> None:
        """Load object info in background."""
        logger.debug(f"_load_object_info called: store={store_name}, name={name}")
        if not self._adapter:
            logger.debug("_load_object_info: no adapter")
            return

        try:
            info = await self._adapter.get_object_info(store_name, name)
            logger.debug(f"Got object info: {info}")
            if info:
                obj_info = ObjectInfo(
                    store=store_name,
                    name=info.name if hasattr(info, "name") else name,
                    size=info.size if hasattr(info, "size") else 0,
                    chunks=info.chunks if hasattr(info, "chunks") else 0,
                    modified=info.mtime if hasattr(info, "mtime") else None,
                    digest=info.digest if hasattr(info, "digest") else None,
                    deleted=info.deleted if hasattr(info, "deleted") else False,
                )
                logger.debug(f"Created ObjectInfo: {obj_info}")
                msg = ObjectInfoLoaded(obj=obj_info)
                self.call_later(lambda m=msg: self._handle_object_info_loaded(m))
            else:
                self.call_later(lambda n=name: self.notify(f"Object '{n}' not found", severity="error"))
        except Exception as e:
            logger.exception(f"Failed to load object info: {e}")
            self.call_later(lambda err=str(e): self.notify(f"Failed to load object info: {err}", severity="error"))

    def _handle_object_info_loaded(self, message: ObjectInfoLoaded) -> None:
        """Handle object info loaded."""
        logger.debug(f"_handle_object_info_loaded: name={message.object.name}")
        object_detail = self.query_one(ObjectDetail)
        object_detail.object_info = message.object

    def on_object_error(self, message: ObjectError) -> None:
        """Handle Object Store error."""
        logger.debug(f"on_object_error: {message.error}")
        self.notify(f"Object Store error: {message.error}", severity="error")

    def _open_object_put_dialog(self) -> None:
        """Open dialog to upload a new object."""
        logger.debug(f"_open_object_put_dialog called, store: {self._selected_object_store}")
        if not self._selected_object_store:
            logger.debug("_open_object_put_dialog: no store selected")
            return
        logger.debug(f"Opening ObjectPutDialog for store: {self._selected_object_store.name}")
        self.push_screen(
            ObjectPutDialog(store_name=self._selected_object_store.name),
            self._handle_object_put_result,
        )

    def _handle_object_put_result(self, result: ObjectPutResult | None) -> None:
        """Handle result from object put dialog."""
        logger.debug(f"_handle_object_put_result called with: {result}")
        if result and self._selected_object_store:
            logger.debug(f"Calling _do_object_put for store={self._selected_object_store.name}, name={result.name}")
            self._do_object_put(
                self._selected_object_store.name,
                result.name,
                result.data,
                result.description,
            )
        else:
            logger.debug(f"Not putting: result={result}, store={self._selected_object_store}")

    @work(exclusive=True, group="object_store")
    async def _do_object_put(
        self, store_name: str, name: str, data: bytes, description: str
    ) -> None:
        """Upload an object in background."""
        logger.debug(f"_do_object_put called: store={store_name}, name={name}, size={len(data)}")
        if not self._adapter:
            logger.debug("_do_object_put: no adapter")
            return

        try:
            logger.debug(f"Calling adapter.put_object({store_name}, {name})")
            await self._adapter.put_object(store_name, name, data, description)
            logger.debug(f"Object put successful: {name}")
            msg = ObjectUploaded(store=store_name, name=name, size=len(data))
            self.call_later(lambda m=msg: self._handle_object_uploaded(m))
        except Exception as e:
            logger.exception(f"Failed to upload object: {e}")
            self.call_later(lambda err=str(e): self.notify(f"Failed to upload object: {err}", severity="error"))

    def on_object_uploaded(self, message: ObjectUploaded) -> None:
        """Handle object uploaded (from message routing)."""
        self._handle_object_uploaded(message)

    def _handle_object_uploaded(self, message: ObjectUploaded) -> None:
        """Handle object uploaded."""
        logger.debug(f"_handle_object_uploaded: store={message.store}, name={message.name}")
        self.notify(f"Uploaded '{message.name}'", severity="information")
        # Reload objects to show new object
        self._load_objects(message.store, offset=self._object_offset)
        # Reload stores to update object count
        self._load_object_stores()

    def _handle_create_object_store_result(self, result: CreateObjectStoreResult | None) -> None:
        """Handle result from create object store dialog."""
        logger.debug(f"_handle_create_object_store_result called with: {result}")
        if result:
            self._do_create_object_store(result)

    @work(exclusive=True, group="object_store")
    async def _do_create_object_store(self, result: CreateObjectStoreResult) -> None:
        """Create an Object Store in background."""
        logger.debug(f"_do_create_object_store called with: {result.name}")
        if not self._adapter:
            logger.debug("_do_create_object_store: no adapter")
            return

        try:
            logger.debug(f"Creating Object Store: {result.name}")
            await self._adapter.create_object_store(
                name=result.name,
                description=result.description,
                ttl=result.ttl,
                max_bytes=result.max_bytes,
                storage=result.storage,
                replicas=result.replicas,
            )
            logger.debug(f"Object Store created successfully: {result.name}")
            self.post_message(ObjectStoreCreated(name=result.name))
        except Exception as e:
            logger.exception(f"Failed to create Object Store: {e}")
            self.post_message(ObjectError(error=f"Failed to create store: {e}"))

    def on_object_store_created(self, message: ObjectStoreCreated) -> None:
        """Handle Object Store created."""
        logger.debug(f"on_object_store_created: {message.name}")
        self.notify(f"Object Store '{message.name}' created", severity="information")
        # Reload stores
        self._load_object_stores()

    @work(exclusive=True, group="object_store")
    async def _do_delete_object_store(self, name: str) -> None:
        """Delete an Object Store in background."""
        if not self._adapter:
            return

        success = await self._adapter.delete_object_store(name)
        if success:
            msg = ObjectStoreDeleted(name=name)
            self.call_later(lambda m=msg: self._handle_object_store_deleted(m))
        else:
            self.call_later(
                lambda: self.notify(f"Failed to delete store '{name}'", severity="error")
            )

    def on_object_store_deleted(self, message: ObjectStoreDeleted) -> None:
        """Handle Object Store deleted (from message routing)."""
        self._handle_object_store_deleted(message)

    def _handle_object_store_deleted(self, message: ObjectStoreDeleted) -> None:
        """Handle Object Store deleted."""
        logger.debug(f"_handle_object_store_deleted: name={message.name}")
        self.notify(f"Object Store '{message.name}' deleted", severity="information")
        self._selected_object_store = None
        self._selected_object = None
        self._object_offset = 0  # Reset pagination
        # Clear object list and detail
        object_list = self.query_one(ObjectList)
        object_list.set_objects("", [])
        object_detail = self.query_one(ObjectDetail)
        object_detail.object_info = None
        # Reload stores
        self._load_object_stores()

    @work(exclusive=True, group="object_store")
    async def _do_delete_object(self, store_name: str, name: str) -> None:
        """Delete an object in background."""
        if not self._adapter:
            return

        success = await self._adapter.delete_object(store_name, name)
        if success:
            msg = ObjectDeleted(store=store_name, name=name)
            self.call_later(lambda m=msg: self._handle_object_deleted(m))
        else:
            self.call_later(
                lambda: self.notify(f"Failed to delete object '{name}'", severity="error")
            )

    def on_object_deleted(self, message: ObjectDeleted) -> None:
        """Handle object deleted (from message routing)."""
        self._handle_object_deleted(message)

    def _handle_object_deleted(self, message: ObjectDeleted) -> None:
        """Handle object deleted."""
        logger.debug(f"_handle_object_deleted: store={message.store}, name={message.name}")
        self.notify(f"Object '{message.name}' deleted", severity="information")
        self._selected_object = None
        # Clear object detail
        object_detail = self.query_one(ObjectDetail)
        object_detail.object_info = None
        # Reload objects (with current pagination offset)
        self._load_objects(message.store, offset=self._object_offset)
        # Reload stores to update object count
        self._load_object_stores()
