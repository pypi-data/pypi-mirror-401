"""NATS adapter wrapping nats.py client."""

import ssl
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from nats.aio.client import Client as NatsClient
from nats.aio.subscription import Subscription
from nats.js import api as js_api
from nats.js.client import JetStreamContext

from nats_tui.exception import NatsTuiConnectionError


@dataclass
class ConnectionConfig:
    """Configuration for NATS connection."""

    server_url: str
    username: str | None = None
    password: str | None = None
    # TLS options
    tls_enabled: bool = False
    tls_ca_cert: str | None = None  # Path to CA certificate
    tls_cert: str | None = None  # Path to client certificate
    tls_key: str | None = None  # Path to client key
    tls_insecure: bool = False  # Disable certificate verification

    def create_tls_context(self) -> ssl.SSLContext | None:
        """Create TLS context based on configuration.

        Returns:
            SSLContext if TLS is enabled, None otherwise
        """
        if not self.tls_enabled:
            return None

        # Create context with secure defaults
        ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

        # Load CA certificate if provided
        if self.tls_ca_cert:
            ca_path = Path(self.tls_ca_cert).expanduser()
            if ca_path.exists():
                ctx.load_verify_locations(str(ca_path))
            else:
                raise NatsTuiConnectionError(
                    msg=f"CA certificate file not found: {self.tls_ca_cert}",
                    title="TLS Configuration Error",
                )

        # Load client certificate and key if provided (mutual TLS)
        if self.tls_cert and self.tls_key:
            cert_path = Path(self.tls_cert).expanduser()
            key_path = Path(self.tls_key).expanduser()
            if not cert_path.exists():
                raise NatsTuiConnectionError(
                    msg=f"Client certificate file not found: {self.tls_cert}",
                    title="TLS Configuration Error",
                )
            if not key_path.exists():
                raise NatsTuiConnectionError(
                    msg=f"Client key file not found: {self.tls_key}",
                    title="TLS Configuration Error",
                )
            ctx.load_cert_chain(str(cert_path), str(key_path))

        # Disable verification if insecure mode (for self-signed certs)
        if self.tls_insecure:
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

        return ctx


class NatsAdapter:
    """Adapter wrapping nats.py client for NATS TUI."""

    def __init__(self, config: ConnectionConfig) -> None:
        self.config = config
        self._client: NatsClient | None = None
        self._subscriptions: list[Subscription] = []
        self._js: JetStreamContext | None = None

    @property
    def is_connected(self) -> bool:
        """Check if currently connected to NATS."""
        return self._client is not None and self._client.is_connected

    @property
    def client(self) -> NatsClient | None:
        """Get the underlying NATS client."""
        return self._client

    @property
    def server_info(self) -> dict[str, Any] | None:
        """Get server info if connected."""
        if self._client and self._client.is_connected:
            info = self._client._server_info
            if info:
                return dict(info)
        return None

    async def connect(self) -> None:
        """Connect to NATS server."""
        self._client = NatsClient()
        try:
            tls_ctx = self.config.create_tls_context()
            await self._client.connect(
                servers=[self.config.server_url],
                user=self.config.username or None,
                password=self.config.password or None,
                tls=tls_ctx,
                connect_timeout=5,
            )
        except NatsTuiConnectionError:
            # Re-raise TLS configuration errors as-is
            self._client = None
            raise
        except Exception as e:
            self._client = None
            error_str = str(e)

            # Provide helpful error messages
            if "authorization" in error_str.lower() or "authentication" in error_str.lower():
                raise NatsTuiConnectionError(
                    msg=f"Authentication failed: {error_str}",
                    title="Authentication Error",
                ) from e
            elif "certificate" in error_str.lower() or "ssl" in error_str.lower():
                hint = " (try --tls-insecure for self-signed certs)" if not self.config.tls_insecure else ""
                raise NatsTuiConnectionError(
                    msg=f"{error_str}{hint}",
                    title="TLS/SSL Error",
                ) from e
            elif "connection refused" in error_str.lower():
                raise NatsTuiConnectionError(
                    msg=f"Connection refused - check server URL and port: {self.config.server_url}",
                    title="Connection Refused",
                ) from e
            else:
                raise NatsTuiConnectionError(
                    msg=error_str,
                    title="Connection Failed",
                ) from e

    async def disconnect(self) -> None:
        """Disconnect from NATS server."""
        if self._client:
            try:
                # Use close() instead of drain() for faster disconnect
                # drain() can hang waiting for pending messages
                await self._client.close()
            except Exception:
                # Ignore errors during disconnect
                pass
            finally:
                self._js = None
                self._client = None

    async def test_connection(self) -> tuple[bool, str]:
        """Test connection without persisting.

        Returns:
            Tuple of (success, message)
        """
        client = NatsClient()
        try:
            tls_ctx = self.config.create_tls_context()
            await client.connect(
                servers=[self.config.server_url],
                user=self.config.username or None,
                password=self.config.password or None,
                tls=tls_ctx,
                connect_timeout=5,
            )
            server_info = client._server_info or {}
            server_id = server_info.get("server_id", "unknown")
            version = server_info.get("version", "unknown")
            tls_status = " (TLS)" if self.config.tls_enabled else ""
            auth_status = " (authenticated)" if self.config.username else ""
            # Use close() instead of drain() for faster test
            await client.close()
            return True, f"Connected{tls_status}{auth_status}! Server: {server_id}, Version: {version}"
        except NatsTuiConnectionError as e:
            # TLS configuration errors from create_tls_context
            return False, f"TLS Error: {e.msg}"
        except Exception as e:
            # Build detailed error message
            error_str = str(e)
            error_type = type(e).__name__

            # Common error patterns with helpful messages
            if "authorization" in error_str.lower() or "authentication" in error_str.lower():
                return False, f"Authentication failed: {error_str}"
            elif "certificate" in error_str.lower() or "ssl" in error_str.lower():
                hint = " (try --tls-insecure for self-signed certs)" if not self.config.tls_insecure else ""
                return False, f"TLS/SSL error: {error_str}{hint}"
            elif "connection refused" in error_str.lower():
                return False, f"Connection refused - check server URL and port: {self.config.server_url}"
            elif "timeout" in error_str.lower():
                return False, f"Connection timed out: {error_str}"
            else:
                return False, f"{error_type}: {error_str}"

    async def subscribe(
        self,
        subject: str,
        callback: Callable[[str, bytes], Awaitable[None]] | None = None,
    ) -> Subscription | None:
        """Subscribe to a subject.

        Args:
            subject: The subject to subscribe to (can include wildcards)
            callback: Async callback called with (subject, data) for each message

        Returns:
            The subscription object, or None if not connected
        """
        if not self._client:
            return None

        async def handler(msg):
            if callback:
                await callback(msg.subject, msg.data)

        sub = await self._client.subscribe(subject, cb=handler)
        self._subscriptions.append(sub)
        return sub

    async def unsubscribe_all(self) -> None:
        """Unsubscribe from all active subscriptions."""
        for sub in self._subscriptions:
            try:
                await sub.unsubscribe()
            except Exception:
                pass
        self._subscriptions.clear()

    async def publish(
        self,
        subject: str,
        payload: bytes,
        headers: dict[str, str] | None = None,
    ) -> None:
        """Publish a message to a subject.

        Args:
            subject: The subject to publish to
            payload: The message payload as bytes
            headers: Optional message headers

        Raises:
            NatsTuiConnectionError: If not connected or publish fails
        """
        if not self._client:
            raise NatsTuiConnectionError(
                msg="Not connected to NATS",
                title="Publish failed",
            )

        await self._client.publish(subject, payload, headers=headers)
        await self._client.flush()

    @property
    def jetstream(self) -> JetStreamContext | None:
        """Get JetStream context, creating it if needed."""
        if self._client and self._client.is_connected and self._js is None:
            # Check if server has a JetStream domain configured
            domain = None
            if self._client._server_info:
                domain = self._client._server_info.get("domain")

            # Use a longer timeout for JetStream operations (default is 5s)
            # Pass domain if configured on the server
            self._js = self._client.jetstream(timeout=30, domain=domain)
        return self._js

    async def list_streams(self) -> list[js_api.StreamInfo]:
        """List all JetStream streams.

        Returns:
            List of StreamInfo objects
        """
        js = self.jetstream
        if not js:
            return []

        try:
            # nats-py 2.x: streams_info() returns List[StreamInfo]
            return await js.streams_info()
        except Exception:
            # JetStream may not be enabled on the server
            return []

    async def get_stream_info(self, name: str) -> js_api.StreamInfo | None:
        """Get stream info by name.

        Args:
            name: Stream name

        Returns:
            StreamInfo or None if not found
        """
        if not self.jetstream:
            return None
        try:
            return await self.jetstream.stream_info(name)
        except Exception:
            return None

    async def get_stream_messages(
        self,
        stream_name: str,
        count: int = 20,
        start_seq: int | None = None,
    ) -> tuple[list[js_api.RawStreamMsg], int, int, int]:
        """Get messages from a stream with pagination info.

        Args:
            stream_name: Name of the stream
            count: Number of messages to retrieve (default 20)
            start_seq: Starting sequence number (None = start from last)

        Returns:
            Tuple of (messages, first_seq, last_seq, total_count)
            - messages: List of RawStreamMsg objects, newest first
            - first_seq: Stream's first sequence number
            - last_seq: Stream's last sequence number
            - total_count: Total messages in stream
        """
        if not self.jetstream:
            return [], 0, 0, 0

        try:
            # Get stream info to know the sequence range
            info = await self.jetstream.stream_info(stream_name)
            if not info or info.state.messages == 0:
                return [], 0, 0, 0

            first_seq = info.state.first_seq
            last_seq = info.state.last_seq
            total_count = info.state.messages

            # Determine starting point
            if start_seq is None:
                # Start from the end (newest messages)
                start = last_seq
            else:
                # Clamp to valid range
                start = min(max(start_seq, first_seq), last_seq)

            # Calculate how far back to go
            end_seq = max(first_seq, start - count + 1)

            messages = []
            # Fetch messages in reverse order (newest first)
            for seq in range(start, end_seq - 1, -1):
                try:
                    msg = await self.jetstream.get_msg(stream_name, seq=seq)
                    if msg:
                        messages.append(msg)
                except Exception:
                    # Message may have been deleted
                    continue

            return messages, first_seq, last_seq, total_count
        except Exception:
            return [], 0, 0, 0

    async def delete_message(self, stream_name: str, seq: int) -> bool:
        """Delete a specific message from a stream.

        Args:
            stream_name: Name of the stream
            seq: Sequence number of the message to delete

        Returns:
            True if deleted successfully, False otherwise
        """
        if not self.jetstream:
            return False

        try:
            return await self.jetstream.delete_msg(stream_name, seq)
        except Exception:
            return False

    async def create_stream(
        self,
        name: str,
        subjects: list[str],
        storage: str = "file",
        retention: str = "limits",
        discard: str = "old",
        max_msgs: int = -1,
        max_bytes: int = -1,
        max_age: float = 0,
        max_msg_size: int = -1,
        max_msgs_per_subject: int = -1,
        num_replicas: int = 1,
        duplicate_window: float = 0,
        allow_rollup: bool = False,
        deny_delete: bool = False,
        deny_purge: bool = False,
    ) -> js_api.StreamInfo:
        """Create a new JetStream stream.

        Args:
            name: Stream name
            subjects: List of subjects to capture
            storage: "file" or "memory"
            retention: "limits", "interest", or "workqueue"
            discard: "old" or "new"
            max_msgs: Max messages (-1 = unlimited)
            max_bytes: Max bytes (-1 = unlimited)
            max_age: Max age in seconds (0 = unlimited)
            max_msg_size: Max message size in bytes (-1 = unlimited)
            max_msgs_per_subject: Max messages per subject (-1 = unlimited)
            num_replicas: Number of replicas (1-5)
            duplicate_window: Duplicate tracking window in seconds (0 = disabled)
            allow_rollup: Allow message roll-ups
            deny_delete: Deny message deletion via API
            deny_purge: Deny stream purging via API

        Returns:
            Created StreamInfo

        Raises:
            NatsTuiConnectionError: If not connected or creation fails
        """
        if not self.jetstream:
            raise NatsTuiConnectionError(
                msg="Not connected to NATS",
                title="Create stream failed",
            )

        # Map storage type
        storage_type = (
            js_api.StorageType.FILE if storage == "file" else js_api.StorageType.MEMORY
        )

        # Map retention policy
        retention_map = {
            "limits": js_api.RetentionPolicy.LIMITS,
            "interest": js_api.RetentionPolicy.INTEREST,
            "workqueue": js_api.RetentionPolicy.WORK_QUEUE,
        }
        retention_policy = retention_map.get(retention, js_api.RetentionPolicy.LIMITS)

        # Map discard policy
        discard_policy = (
            js_api.DiscardPolicy.NEW if discard == "new" else js_api.DiscardPolicy.OLD
        )

        config = js_api.StreamConfig(
            name=name,
            subjects=subjects,
            storage=storage_type,
            retention=retention_policy,
            discard=discard_policy,
            max_msgs=max_msgs if max_msgs > 0 else -1,
            max_bytes=max_bytes if max_bytes > 0 else -1,
            max_age=max_age if max_age > 0 else None,
            max_msg_size=max_msg_size if max_msg_size > 0 else -1,
            max_msgs_per_subject=max_msgs_per_subject if max_msgs_per_subject > 0 else -1,
            num_replicas=num_replicas,
            duplicate_window=duplicate_window if duplicate_window > 0 else 0,
            allow_rollup_hdrs=allow_rollup,
            deny_delete=deny_delete,
            deny_purge=deny_purge,
        )
        return await self.jetstream.add_stream(config)

    async def delete_stream(self, name: str) -> bool:
        """Delete a JetStream stream.

        Args:
            name: Stream name

        Returns:
            True if deleted successfully
        """
        if not self.jetstream:
            return False
        try:
            return await self.jetstream.delete_stream(name)
        except Exception:
            return False

    async def purge_stream(
        self, name: str, subject: str | None = None, keep: int | None = None
    ) -> bool:
        """Purge messages from a stream.

        Args:
            name: Stream name
            subject: Only purge this subject (optional)
            keep: Keep only this many recent messages (optional)

        Returns:
            True if purged successfully
        """
        if not self.jetstream:
            return False
        try:
            return await self.jetstream.purge_stream(name, subject=subject, keep=keep)
        except Exception:
            return False

    # Consumer Management

    async def list_consumers(self, stream: str) -> list[js_api.ConsumerInfo]:
        """List all consumers for a stream.

        Args:
            stream: Stream name

        Returns:
            List of ConsumerInfo objects
        """
        if not self.jetstream:
            return []
        try:
            return await self.jetstream.consumers_info(stream)
        except Exception:
            return []

    async def get_consumer_info(
        self, stream: str, consumer: str
    ) -> js_api.ConsumerInfo | None:
        """Get consumer info.

        Args:
            stream: Stream name
            consumer: Consumer name

        Returns:
            ConsumerInfo or None if not found
        """
        if not self.jetstream:
            return None
        try:
            return await self.jetstream.consumer_info(stream, consumer)
        except Exception:
            return None

    async def create_consumer(
        self,
        stream: str,
        name: str,
        durable_name: str | None = None,
        deliver_policy: str = "all",
        ack_policy: str = "explicit",
        filter_subject: str | None = None,
    ) -> js_api.ConsumerInfo:
        """Create a new consumer.

        Args:
            stream: Stream name
            name: Consumer name
            durable_name: Durable name (optional)
            deliver_policy: "all", "new", or "last"
            ack_policy: "explicit", "none", or "all"
            filter_subject: Subject filter (optional)

        Returns:
            Created ConsumerInfo

        Raises:
            NatsTuiConnectionError: If not connected or creation fails
        """
        if not self.jetstream:
            raise NatsTuiConnectionError(
                msg="Not connected to NATS",
                title="Create consumer failed",
            )

        # Map string policies to enums
        deliver_map = {
            "all": js_api.DeliverPolicy.ALL,
            "new": js_api.DeliverPolicy.NEW,
            "last": js_api.DeliverPolicy.LAST,
        }
        ack_map = {
            "explicit": js_api.AckPolicy.EXPLICIT,
            "none": js_api.AckPolicy.NONE,
            "all": js_api.AckPolicy.ALL,
        }

        config = js_api.ConsumerConfig(
            name=name,
            durable_name=durable_name or name,
            deliver_policy=deliver_map.get(deliver_policy, js_api.DeliverPolicy.ALL),
            ack_policy=ack_map.get(ack_policy, js_api.AckPolicy.EXPLICIT),
            filter_subject=filter_subject if filter_subject else None,
        )
        return await self.jetstream.add_consumer(stream, config=config)

    async def delete_consumer(self, stream: str, consumer: str) -> bool:
        """Delete a consumer.

        Args:
            stream: Stream name
            consumer: Consumer name

        Returns:
            True if deleted successfully
        """
        if not self.jetstream:
            return False
        try:
            return await self.jetstream.delete_consumer(stream, consumer)
        except Exception:
            return False

    async def pause_consumer(self, stream: str, consumer: str) -> bool:
        """Pause a consumer.

        Args:
            stream: Stream name
            consumer: Consumer name

        Returns:
            True if paused successfully
        """
        if not self.jetstream:
            return False
        try:
            from datetime import datetime, timedelta, timezone

            # Pause for a very long time (effectively indefinite)
            pause_until = (
                datetime.now(timezone.utc) + timedelta(days=365 * 100)
            ).strftime("%Y-%m-%dT%H:%M:%SZ")
            result = await self.jetstream.pause_consumer(stream, consumer, pause_until)
            return result.paused
        except Exception:
            return False

    async def resume_consumer(self, stream: str, consumer: str) -> bool:
        """Resume a paused consumer.

        Args:
            stream: Stream name
            consumer: Consumer name

        Returns:
            True if resumed successfully
        """
        if not self.jetstream:
            return False
        try:
            result = await self.jetstream.resume_consumer(stream, consumer)
            return not result.paused
        except Exception:
            return False
