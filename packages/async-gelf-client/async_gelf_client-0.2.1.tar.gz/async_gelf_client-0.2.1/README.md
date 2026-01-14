# Async GELF Client

Fully async UDP client for sending GELF messages to Graylog. Uses native asyncio for maximum performance, automatically compresses messages larger than 8KB, and runs all blocking operations in thread pool to avoid blocking the event loop.

## Installation

```bash
pip install async-gelf-client
```

## Usage

```python
import asyncio
from asyncgelf import AsyncGelfClient, GelfMessage

async def main():
    client = AsyncGelfClient(host="localhost", port=12201)
    
    message = GelfMessage.create(
        short_message="Hello Graylog",
        level=6,
        host="myapp"
    )
    
    await client.send(message)

asyncio.run(main())
```

### Parallel sending (high performance)

```python
import asyncio
from asyncgelf import AsyncGelfClient, GelfMessage

async def main():
    client = AsyncGelfClient(host="localhost", port=12201)
    
    # Send multiple messages in parallel without blocking
    messages = [
        GelfMessage.create(short_message=f"Message {i}", level=6, host="myapp")
        for i in range(100)
    ]
    
    await asyncio.gather(*[client.send(msg) for msg in messages])

asyncio.run(main())
```

## API

### AsyncGelfClient

Fully async UDP client for sending GELF messages. All blocking operations (JSON serialization, gzip compression) run in thread pool.

**Parameters:**

- `host` (str): Graylog server hostname or IP address
- `port` (int): UDP port (default: 12201)
- `compress_threshold` (int): Message size in bytes to trigger compression (default: 8192)

**Methods:**

- `async send(message: dict[str, Any]) -> None`: Sends GELF message

### GelfMessage

GELF message builder with static methods.

**Methods:**

#### `GelfMessage.create(...)`

Creates a properly formatted GELF message.

**Parameters:**

- `short_message` (str): Short log description (required)
- `full_message` (str | None): Full log description (optional)
- `level` (int): Syslog level (7=debug, 6=info, 4=warning, 3=error, 2=critical)
- `host` (str): Host/application name
- `timestamp` (float | None): Unix timestamp (if None - current time)
- `**additional_fields`: Additional fields (will be prefixed with _)

**Returns:** dict with GELF message

#### `GelfMessage.convert_log_level(python_level)`

Converts Python logging level to Syslog level for GELF.

**Parameters:**

- `python_level` (int): Python logging level (logging.DEBUG, logging.INFO, etc.)

**Returns:** int - Syslog level

## Requirements

- Python >= 3.10

## License

MIT
