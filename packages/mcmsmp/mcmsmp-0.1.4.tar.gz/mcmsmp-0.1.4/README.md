# mcmsmp - Minecraft Management Server Protocol Client

Python client for Minecraft Management Server Protocol (MCMSP).

## Installation

```pip install mcmsmp```

## Quick Start


```bash
import asyncio
from mcmsmp import MinecraftManagementClient
import mcmsmp

async def main():
    client = MinecraftManagementClient(
        uri="ws://localhost:25568",
        secret="your_secret_key"
    )
      
    @client.on_notification(mcmsmp.notifications.types.PlayerJoin)
    async def onPlayerJoin(e: mcmsmp.notifications.types.PlayerJoin):
        print(f"e res: {e.player.name}")
    
    await client.connect()
    
    # Get online players
    players = await client.rpc(mcmsmp.trigger.types.get.PLAYERS)
    print(f"Online players: {players}")
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Documentation
See [examples](https://github.com/DngYnQ/mcmsmp/tree/master/examples) for more usage examples.

