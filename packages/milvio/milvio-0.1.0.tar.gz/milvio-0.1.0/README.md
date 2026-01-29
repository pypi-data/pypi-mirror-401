# Milvio Redis Service

A simple wrapper around `redis-py` providing both async and sync clients with automatic prefixing for app slug and environment.

## Installation

```bash
pip install milvio_redis
```

## Usage

```python
import asyncio
from milvio_redis import redis_service

async def main():
    # Connect
    await redis_service.connect(
        redis_url="redis://localhost:6379/1",
        app_slug="my_app",
        environment="production"
    )

    # Set value (will be prefixed as my_app_production_key1)
    await redis_service.set_async("key1", "value1")

    # Get value
    value = await redis_service.get_async("key1")
    print(value)
    
    # Disconnect
    await redis_service.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```
