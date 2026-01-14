# Async GELF Client

Async UDP client for sending GELF messages to Graylog. Uses native asyncio for maximum performance and automatically compresses messages larger than 8KB.

## Installation

```bash
pip install async-gelf-client
```

## Usage

```python
import asyncio
from async_gelf_client import AsyncGelfUdpClient, create_gelf_message

async def main():
    client = AsyncGelfUdpClient(host="localhost", port=12201)
    
    message = create_gelf_message(
        short_message="Hello Graylog",
        level=6,
        host="myapp"
    )
    
    await client.send(message)

asyncio.run(main())
```

## API

### AsyncGelfUdpClient

Async UDP client for sending GELF messages.

**Parameters:**

- `host` (str): Graylog server hostname or IP address
- `port` (int): UDP port (default: 12201)
- `compress_threshold` (int): Message size in bytes to trigger compression (default: 8192)

**Methods:**

- `async send(message: dict[str, Any]) -> None`: Sends GELF message

### create_gelf_message

Creates a properly formatted GELF message.

**Parameters:**

- `short_message` (str): Short log description (required)
- `full_message` (str | None): Full log description (optional)
- `level` (int): Syslog level (7=debug, 6=info, 4=warning, 3=error, 2=critical)
- `host` (str): Host/application name
- `timestamp` (float | None): Unix timestamp (if None - current time)
- `**additional_fields`: Additional fields (will be prefixed with _)

**Returns:** dict with GELF message

### convert_python_log_level

Converts Python logging level to Syslog level for GELF.

**Parameters:**

- `python_level` (int): Python logging level (logging.DEBUG, logging.INFO, etc.)

**Returns:** int - Syslog level

## Requirements

- Python >= 3.10

## License

MIT
