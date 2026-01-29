#!/usr/bin/env python3
import asyncio
import builtins
import nest_asyncio
import sys

nest_asyncio.apply()
builtins.input = lambda *args: ""

sys.path.insert(0, 'src')
from sphero_rvr_mcp.api import RVRClient

async def main():
    client = RVRClient(log_level="WARNING", log_format="console")

    try:
        print("🔌 Connecting to RVR...")
        await client.initialize()
        result = await client.connect()

        if not result.get("success"):
            print(f"❌ Connection failed: {result.get('error')}")
            return

        print("✅ Connected!")

        print("\n☀️  Reading ambient light sensor...")
        light_result = await client.get_ambient_light()

        if light_result.get("success"):
            light_value = light_result.get('light_value', 0)
            print(f"\n✅ Ambient Light: {light_value:.2f}")
        else:
            print(f"❌ Ambient light failed: {light_result.get('error')}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🔌 Disconnecting...")
        await client.shutdown()
        print("✅ Done!")

asyncio.run(main())
