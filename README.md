# Healthchecks

An asynchronous Python client for interacting with [Healthchecks.io](https://healthchecks.io), enabling seamless integration using async context managers.

## Installation

Install directly from GitHub:

```sh
pip install git+https://github.com/yourusername/healthchecks.git
```

## Usage

```python
from aiohttp import ClientSession
from healthchecks import Healthchecks

healthchecks = Healthchecks(
    http=ClientSession(),
    ping_key="your-secret-ping-key"
)

async with healthchecks.ping(slug="your-check-slug"):
    # Your monitored code here
    pass
```

If an exception occurs within the monitored block, the failure is automatically reported to the `/fail` endpoint.

## Features

- **Async support**: Fully asynchronous with `asyncio` and `aiohttp`
- **Context manager**: Automatically pings and finalizes checks
- **Single dependency**: Only requires `aiohttp`
- **Automatic failure reporting**: Exceptions trigger reporting to the `/fail` endpoint
