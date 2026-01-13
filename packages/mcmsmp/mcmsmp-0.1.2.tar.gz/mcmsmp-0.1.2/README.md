# mcmsmp - Minecraft Management Server Protocol Client

Python client for Minecraft Management Server Protocol (MCMSP).

## Installation

```pip install mcmsmp```

## Quick Start


```bash
import asyncio
from mcmsmp import MinecraftManagementClient

async def main():
    client = MinecraftManagementClient(
        uri="ws://localhost:8080",
        secret="your_secret_key"
    )
    
    await client.connect()
    
    # Get online players
    players = await client.rpc("minecraft:players")
    print(f"Online players: {players}")
    
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Documentation
See [examples](https://github.com/DngYnQ/mcmsmp/tree/master/examples) for more usage examples.

