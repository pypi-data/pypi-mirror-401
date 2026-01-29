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

        print("\n🔴 Setting LEDs to RED...")
        led_result = await client.set_all_leds(255, 0, 0)

        if led_result.get("success"):
            print(f"✅ SUCCESS! LEDs are now RED! 🔴")
            print(f"   RGB: ({led_result['red']}, {led_result['green']}, {led_result['blue']})")
        else:
            print(f"❌ LED command failed: {led_result.get('error')}")

        await asyncio.sleep(2)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🔌 Disconnecting...")
        await client.shutdown()
        print("✅ Done!")

asyncio.run(main())
