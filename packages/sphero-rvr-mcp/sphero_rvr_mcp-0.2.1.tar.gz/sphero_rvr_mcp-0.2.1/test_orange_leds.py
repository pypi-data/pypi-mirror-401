#!/usr/bin/env python3
"""Test script to set RVR LEDs to orange using the new architecture."""

import asyncio
import sys
sys.path.insert(0, 'src')

from sphero_rvr_mcp.api import quick_connect


async def main():
    """Set LEDs to orange."""
    client = None
    try:
        print("🔌 Connecting to RVR...")
        client = await quick_connect(log_level="INFO")
        print("✅ Connected!")

        print("\n🟠 Setting LEDs to orange...")
        result = await client.set_all_leds(red=255, green=165, blue=0)

        if result.get("success"):
            print(f"✅ LEDs set to orange! RGB: ({result['red']}, {result['green']}, {result['blue']})")
        else:
            print(f"❌ Failed: {result.get('error')}")

        # Wait a moment to see the lights
        await asyncio.sleep(2)

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if client:
            print("\n🔌 Disconnecting...")
            await client.shutdown()
            print("✅ Done!")


if __name__ == "__main__":
    asyncio.run(main())
