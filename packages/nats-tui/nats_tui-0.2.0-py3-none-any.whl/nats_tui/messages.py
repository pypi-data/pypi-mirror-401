"""Custom message classes for NATS TUI events."""

from dataclasses import dataclass
from datetime import datetime

from textual.message import Message


class NatsConnecting(Message):
    """Posted when connection attempt starts."""

    def __init__(self, server_url: str) -> None:
        super().__init__()
        self.server_url = server_url


class NatsConnected(Message):
    """Posted when connection is established."""

    def __init__(self, server_url: str, server_info: dict) -> None:
        super().__init__()
        self.server_url = server_url
        self.server_info = server_info


class NatsDisconnected(Message):
    """Posted when connection is closed."""

    pass


class NatsConnectionFailed(Message):
    """Posted when connection attempt fails."""

    def __init__(self, server_url: str, error: Exception) -> None:
        super().__init__()
        self.server_url = server_url
        self.error = error


class NatsConnectionTested(Message):
    """Posted when test connection completes."""

    def __init__(self, success: bool, message: str) -> None:
        super().__init__()
        self.success = success
        self.message = message


class SubjectDiscovered(Message):
    """Posted when a message is received on a subject."""

    def __init__(self, subject: str, data: bytes) -> None:
        super().__init__()
        self.subject = subject
        self.data = data


class SubjectSelected(Message):
    """Posted when a subject is selected in the tree."""

    def __init__(self, full_subject: str, message_count: int) -> None:
        super().__init__()
        self.full_subject = full_subject
        self.message_count = message_count


class SubjectsCleared(Message):
    """Posted when subject list is cleared."""

    pass


class MessagePublished(Message):
    """Posted when a message is successfully published."""

    def __init__(self, subject: str) -> None:
        super().__init__()
        self.subject = subject


class MessagePublishFailed(Message):
    """Posted when publishing fails."""

    def __init__(self, subject: str, error: str) -> None:
        super().__init__()
        self.subject = subject
        self.error = error


@dataclass
class ReceivedMessage:
    """A message received from NATS subscription."""

    subject: str
    payload: bytes
    timestamp: datetime
    size: int

    @property
    def payload_str(self) -> str:
        """Get payload as string, handling decode errors."""
        try:
            return self.payload.decode("utf-8")
        except UnicodeDecodeError:
            return f"<binary data: {self.size} bytes>"

    @property
    def preview(self) -> str:
        """Get a short preview of the payload."""
        text = self.payload_str
        if len(text) > 50:
            return text[:47] + "..."
        return text


class SubscriptionStarted(Message):
    """Posted when subscription to a subject starts."""

    def __init__(self, subject: str) -> None:
        super().__init__()
        self.subject = subject


class SubscriptionStopped(Message):
    """Posted when subscription stops."""

    pass


class MessageReceived(Message):
    """Posted when a message is received on the active subscription."""

    def __init__(self, received_message: ReceivedMessage) -> None:
        super().__init__()
        self.received_message = received_message


# JetStream Stream Messages


@dataclass
class StreamInfo:
    """Stream information for display."""

    name: str
    subjects: list[str]
    messages: int
    bytes: int
    storage: str  # "file" or "memory"
    retention: str  # "limits", "interest", "workqueue"
    consumers: int
    first_seq: int
    last_seq: int
    max_msgs: int
    max_bytes: int
    max_age: float  # seconds, 0 = unlimited


class StreamsLoaded(Message):
    """Posted when streams list is loaded."""

    def __init__(self, streams: list[StreamInfo]) -> None:
        super().__init__()
        self.streams = streams


class StreamSelected(Message):
    """Posted when a stream is selected."""

    def __init__(self, stream: StreamInfo) -> None:
        super().__init__()
        self.stream = stream


class StreamCreated(Message):
    """Posted when a stream is created."""

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name


class StreamDeleted(Message):
    """Posted when a stream is deleted."""

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name


class StreamPurged(Message):
    """Posted when a stream is purged."""

    def __init__(self, name: str, messages_removed: int) -> None:
        super().__init__()
        self.name = name
        self.messages_removed = messages_removed


class StreamError(Message):
    """Posted when a stream operation fails."""

    def __init__(self, error: str) -> None:
        super().__init__()
        self.error = error


# JetStream Consumer Messages


@dataclass
class ConsumerInfo:
    """Consumer information for display."""

    name: str
    stream_name: str
    durable_name: str | None
    deliver_policy: str
    ack_policy: str
    filter_subject: str | None
    num_pending: int
    num_waiting: int
    num_ack_pending: int
    num_redelivered: int
    max_deliver: int
    paused: bool


class ConsumersLoaded(Message):
    """Posted when consumers list is loaded."""

    def __init__(self, stream_name: str, consumers: list[ConsumerInfo]) -> None:
        super().__init__()
        self.stream_name = stream_name
        self.consumers = consumers


class ConsumerSelected(Message):
    """Posted when a consumer is selected."""

    def __init__(self, consumer: ConsumerInfo) -> None:
        super().__init__()
        self.consumer = consumer


class ConsumerCreated(Message):
    """Posted when a consumer is created."""

    def __init__(self, stream_name: str, consumer_name: str) -> None:
        super().__init__()
        self.stream_name = stream_name
        self.consumer_name = consumer_name


class ConsumerDeleted(Message):
    """Posted when a consumer is deleted."""

    def __init__(self, stream_name: str, consumer_name: str) -> None:
        super().__init__()
        self.stream_name = stream_name
        self.consumer_name = consumer_name


class ConsumerPaused(Message):
    """Posted when a consumer pause state changes."""

    def __init__(self, stream_name: str, consumer_name: str, paused: bool) -> None:
        super().__init__()
        self.stream_name = stream_name
        self.consumer_name = consumer_name
        self.paused = paused


class ConsumerError(Message):
    """Posted when a consumer operation fails."""

    def __init__(self, error: str) -> None:
        super().__init__()
        self.error = error


# Stream Message Browser Messages


@dataclass
class StreamMessageInfo:
    """A message stored in a JetStream stream."""

    seq: int
    subject: str
    data: bytes | None
    time: datetime | None
    headers: dict[str, str] | None

    @property
    def data_str(self) -> str:
        """Get data as string, handling decode errors."""
        if self.data is None:
            return "<no data>"
        try:
            return self.data.decode("utf-8")
        except UnicodeDecodeError:
            return f"<binary data: {len(self.data)} bytes>"

    @property
    def preview(self) -> str:
        """Get a short preview of the data."""
        text = self.data_str
        # Remove newlines for preview
        text = text.replace("\n", " ").replace("\r", "")
        if len(text) > 60:
            return text[:57] + "..."
        return text

    @property
    def size(self) -> int:
        """Get the size of the data in bytes."""
        return len(self.data) if self.data else 0


class StreamMessagesLoaded(Message):
    """Posted when stream messages are loaded."""

    def __init__(
        self,
        stream_name: str,
        messages: list[StreamMessageInfo],
        first_seq: int = 0,
        last_seq: int = 0,
        total_count: int = 0,
        page_start_seq: int | None = None,
    ) -> None:
        super().__init__()
        self.stream_name = stream_name
        self.messages = messages
        # Pagination info
        self.first_seq = first_seq  # Stream's first message seq
        self.last_seq = last_seq  # Stream's last message seq
        self.total_count = total_count  # Total messages in stream
        self.page_start_seq = page_start_seq  # Starting seq of this page


class StreamMessageSelected(Message):
    """Posted when a stream message is selected."""

    def __init__(self, message: StreamMessageInfo) -> None:
        super().__init__()
        self.message = message


class StreamMessageDeleted(Message):
    """Posted when a stream message is deleted."""

    def __init__(self, stream_name: str, seq: int) -> None:
        super().__init__()
        self.stream_name = stream_name
        self.seq = seq
