#!/usr/bin/env python3
"""Test all SDK response keys to ensure correct parsing."""
import asyncio
import nest_asyncio
nest_asyncio.apply()

from sphero_sdk import SpheroRvrAsync, SerialAsyncDal

async def main():
    loop = asyncio.get_running_loop()
    dal = SerialAsyncDal(loop=loop, device='/dev/ttyS0', baud=115200)
    rvr = SpheroRvrAsync(dal=dal)

    try:
        await rvr.wake()
        await asyncio.sleep(2)

        print("=" * 60)
        print("SDK RESPONSE KEY VERIFICATION")
        print("=" * 60)

        # Battery percentage
        print("\n1. get_battery_percentage()")
        result = await rvr.get_battery_percentage()
        print(f"   Keys: {list(result.keys())}")
        print(f"   Expected: ['percentage']")
        print(f"   ✓ CORRECT" if 'percentage' in result else f"   ✗ WRONG")

        # Battery voltage state
        print("\n2. get_battery_voltage_state()")
        result = await rvr.get_battery_voltage_state()
        print(f"   Keys: {list(result.keys())}")
        print(f"   Expected: ['state']")
        print(f"   ✓ CORRECT" if 'state' in result else f"   ✗ WRONG")

        # Ambient light
        print("\n3. get_ambient_light_sensor_value()")
        result = await rvr.get_ambient_light_sensor_value()
        print(f"   Keys: {list(result.keys())}")
        print(f"   Expected: ['ambientLightValue']")
        print(f"   ✓ CORRECT" if 'ambientLightValue' in result else f"   ✗ WRONG")

        # Color detection
        print("\n4. get_rgbc_sensor_values()")
        await rvr.enable_color_detection(is_enabled=True)
        await asyncio.sleep(0.1)
        result = await rvr.get_rgbc_sensor_values()
        await rvr.enable_color_detection(is_enabled=False)
        print(f"   Keys: {list(result.keys())}")
        print(f"   Expected: ['redChannelValue', 'greenChannelValue', 'blueChannelValue', 'clearChannelValue']")
        all_present = all(k in result for k in ['redChannelValue', 'greenChannelValue', 'blueChannelValue', 'clearChannelValue'])
        print(f"   ✓ CORRECT" if all_present else f"   ✗ WRONG")

        # Bluetooth name
        print("\n5. get_bluetooth_advertising_name()")
        result = await rvr.get_bluetooth_advertising_name()
        print(f"   Keys: {list(result.keys())}")
        print(f"   Expected: ['name']")
        print(f"   ✓ CORRECT" if 'name' in result else f"   ✗ WRONG")

        print("\n" + "=" * 60)
        print("VERIFICATION COMPLETE")
        print("=" * 60)

        await rvr.close()

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(main())
