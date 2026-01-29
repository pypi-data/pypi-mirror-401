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
    client = RVRClient(log_level="INFO", log_format="console")  # More verbose logging

    try:
        print("🔌 Connecting to RVR...")
        await client.initialize()
        result = await client.connect()

        if not result.get("success"):
            print(f"❌ Connection failed: {result.get('error')}")
            return

        print("✅ Connected!")

        # Try with longer stabilization
        print("\n🎨 Detecting color under rover (200ms stabilization)...")
        color_result = await client.get_color_detection(stabilization_ms=200)

        print(f"\nFull response: {color_result}")

        if color_result.get("success"):
            r = color_result.get('r', 0)
            g = color_result.get('g', 0)
            b = color_result.get('b', 0)
            c = color_result.get('c', 0)

            print(f"\n✅ Color detected!")
            print(f"   Red:   {r}")
            print(f"   Green: {g}")
            print(f"   Blue:  {b}")
            print(f"   Clear: {c}")
        else:
            print(f"❌ Color detection failed: {color_result.get('error')}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🔌 Disconnecting...")
        await client.shutdown()
        print("✅ Done!")

asyncio.run(main())
