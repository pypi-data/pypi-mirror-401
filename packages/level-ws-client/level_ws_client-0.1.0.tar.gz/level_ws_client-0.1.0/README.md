# level-ws-client

Async WebSocket and HTTP client for the Level Lock API.

## Installation

```bash
pip install level-ws-client
```

## Usage

### HTTP Client

```python
import asyncio
from aiohttp import ClientSession
from level_ws_client import Client

async def main():
    async def get_token() -> str:
        return "your-api-token"

    async with ClientSession() as session:
        client = Client(session, "https://api.level.co", get_token)
        locks = await client.async_list_locks()
        print(locks)

asyncio.run(main())
```

### WebSocket Client

```python
import asyncio
from aiohttp import ClientSession
from level_ws_client import LevelWebsocketManager

async def on_state_update(device_uuid: str, is_locked: bool | None, state: dict | None):
    print(f"Device {device_uuid}: locked={is_locked}")

async def main():
    async def get_token() -> str:
        return "your-api-token"

    async with ClientSession() as session:
        ws = LevelWebsocketManager(
            session,
            "https://api.level.co",
            get_token,
            on_state_update,
        )
        await ws.async_start()
        devices = await ws.async_get_devices()
        print(devices)
        await ws.async_stop()

asyncio.run(main())
```

## Development

```bash
uv sync --all-extras --dev
uv run ruff check .
uv run black .
```

## License

MIT
