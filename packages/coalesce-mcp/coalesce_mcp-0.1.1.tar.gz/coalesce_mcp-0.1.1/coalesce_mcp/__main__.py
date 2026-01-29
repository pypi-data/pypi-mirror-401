# Create the __main__.py
import asyncio
from coalesce_mcp.server import main

if __name__ == "__main__":
    asyncio.run(main())