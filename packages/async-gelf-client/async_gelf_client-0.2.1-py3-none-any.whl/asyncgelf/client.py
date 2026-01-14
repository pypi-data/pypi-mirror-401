import asyncio
import gzip
import json
from typing import Any


class AsyncGelfClient:
    """Async UDP client for sending GELF messages to Graylog.

    Uses native asyncio for maximum performance without threads.
    Automatically compresses messages larger than 8KB (Graylog standard).
    All blocking operations run in thread pool to avoid blocking event loop.
    """

    MAX_CHUNK_SIZE = 8192

    def __init__(self, host: str, port: int = 12201, compress_threshold: int = 8192) -> None:
        """Initialize GELF UDP client.

        Args:
            host: Graylog server hostname or IP address
            port: UDP port (default: 12201)
            compress_threshold: Message size in bytes to trigger compression (default: 8192)
        """
        self.host = host
        self.port = port
        self.compress_threshold = compress_threshold

    async def send(self, message: dict[str, Any]) -> None:
        """Send GELF message to Graylog via UDP.

        Args:
            message: GELF message dict with fields like version, host, short_message, etc.

        Raises:
            Exception: On send error (logged but doesn't interrupt execution)
        """
        try:
            # Serialize JSON in thread pool to avoid blocking
            message_bytes = await asyncio.to_thread(
                lambda: json.dumps(message).encode('utf-8')
            )

            # Compress in thread pool if message is large
            if len(message_bytes) > self.compress_threshold:
                message_bytes = await asyncio.to_thread(gzip.compress, message_bytes)

            # Create async UDP connection
            loop = asyncio.get_event_loop()
            transport, _ = await loop.create_datagram_endpoint(
                lambda: asyncio.DatagramProtocol(),
                remote_addr=(self.host, self.port)
            )

            try:
                transport.sendto(message_bytes)
                await asyncio.sleep(0.001)
            finally:
                transport.close()

        except Exception as e:
            print(f"[AsyncGelfClient] Failed to send message: {e}")
