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

        print("\n🎨 Reading color sensor...")
        color_result = await client.get_color_detection(stabilization_ms=100)

        if color_result.get("success"):
            r = color_result.get('r', 0)
            g = color_result.get('g', 0)
            b = color_result.get('b', 0)
            c = color_result.get('c', 0)

            print(f"\n✅ Color sensor readings:")
            print(f"   Red:   {r}")
            print(f"   Green: {g}")
            print(f"   Blue:  {b}")
            print(f"   Clear: {c}")

            # Identify the dominant color
            max_val = max(r, g, b)
            if max_val < 100:
                color_name = "DARK/BLACK"
            elif r > g and r > b:
                if r > g * 1.3:
                    color_name = "RED"
                elif g > b:
                    color_name = "ORANGE/YELLOW"
                else:
                    color_name = "REDDISH"
            elif g > r and g > b:
                if g > r * 1.3:
                    color_name = "GREEN"
                else:
                    color_name = "GREENISH"
            elif b > r and b > g:
                if b > g * 1.3:
                    color_name = "BLUE"
                else:
                    color_name = "BLUISH"
            elif r > 200 and g > 200 and b > 200:
                color_name = "WHITE/LIGHT"
            else:
                color_name = "MIXED/NEUTRAL"

            print(f"\n🎨 Surface color: {color_name}")
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
