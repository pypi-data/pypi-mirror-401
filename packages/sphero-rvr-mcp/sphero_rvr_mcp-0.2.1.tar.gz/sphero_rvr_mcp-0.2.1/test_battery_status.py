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

        # Test battery status
        print("\n🔋 Getting battery status...")
        battery = await client._sensor_service.get_battery_status()

        if battery.get("success"):
            print(f"\n✅ Battery Status:")
            print(f"   Percentage: {battery.get('percentage')}%")
            print(f"   Voltage State: {battery.get('voltage_state')}")
        else:
            print(f"❌ Battery status failed: {battery.get('error')}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🔌 Disconnecting...")
        await client.shutdown()
        print("✅ Done!")

asyncio.run(main())
