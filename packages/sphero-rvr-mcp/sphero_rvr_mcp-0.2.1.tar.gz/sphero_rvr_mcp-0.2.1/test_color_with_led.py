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

        # Turn on belly LED
        print("\n💡 Turning ON belly LED...")
        await client.enable_color_detection(enabled=True)

        # Wait for it to stabilize
        await asyncio.sleep(0.5)

        # Read the color values directly from SDK
        print("\n🎨 Reading color sensor...")
        rvr = client.connection_manager.rvr
        color_data = await rvr.get_rgbc_sensor_values()

        r = color_data.get('r', 0)
        g = color_data.get('g', 0)
        b = color_data.get('b', 0)
        c = color_data.get('c', 0)

        print(f"\n✅ Color sensor readings:")
        print(f"   Red:   {r}")
        print(f"   Green: {g}")
        print(f"   Blue:  {b}")
        print(f"   Clear: {c}")

        # Identify the color
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
            # More detailed color
            if r > 150 and g > 100 and b < 100:
                print(f"\n🎨 The surface appears to be ORANGE/BROWN")
            elif r > 100 and g > 100 and b < 80:
                print(f"\n🎨 The surface appears to be YELLOW/TAN")
            else:
                print(f"\n🎨 The surface has a mixed color")

        # Turn off belly LED
        print("\n💡 Turning OFF belly LED...")
        await client.enable_color_detection(enabled=False)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🔌 Disconnecting...")
        await client.shutdown()
        print("✅ Done!")

asyncio.run(main())
