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

        print("\n🎨 Detecting color under rover...")
        color_result = await client.get_color_detection()

        if color_result.get("success"):
            r = color_result.get('r', 0)
            g = color_result.get('g', 0)
            b = color_result.get('b', 0)
            c = color_result.get('c', 0)

            print(f"✅ Color detected!")
            print(f"   Red:   {r}")
            print(f"   Green: {g}")
            print(f"   Blue:  {b}")
            print(f"   Clear: {c}")

            # Simple color identification
            if r > g and r > b:
                if r > 100:
                    print(f"\n🎨 The surface appears to be REDDISH")
            elif g > r and g > b:
                if g > 100:
                    print(f"\n🎨 The surface appears to be GREENISH")
            elif b > r and b > g:
                if b > 100:
                    print(f"\n🎨 The surface appears to be BLUISH")
            elif r < 50 and g < 50 and b < 50:
                print(f"\n🎨 The surface appears to be DARK/BLACK")
            elif r > 200 and g > 200 and b > 200:
                print(f"\n🎨 The surface appears to be LIGHT/WHITE")
            else:
                print(f"\n🎨 The surface has a mixed color")
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
