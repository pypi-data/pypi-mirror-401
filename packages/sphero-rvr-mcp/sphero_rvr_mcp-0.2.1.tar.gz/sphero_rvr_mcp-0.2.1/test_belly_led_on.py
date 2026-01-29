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

        print("\n💡 Turning ON belly LED...")
        led_result = await client.enable_color_detection(enabled=True)

        if led_result.get("success"):
            print(f"✅ Belly LED is now ON! 💡")
        else:
            print(f"❌ Failed to turn on belly LED: {led_result.get('error')}")

        print("\nBelly LED will stay on until you disconnect or turn it off.")
        print("Press Ctrl+C when ready to disconnect...")

        # Keep running
        await asyncio.sleep(300)  # 5 minutes max

    except KeyboardInterrupt:
        print("\n\n⌨️  Keyboard interrupt received")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🔌 Disconnecting...")
        await client.shutdown()
        print("✅ Done!")

asyncio.run(main())
