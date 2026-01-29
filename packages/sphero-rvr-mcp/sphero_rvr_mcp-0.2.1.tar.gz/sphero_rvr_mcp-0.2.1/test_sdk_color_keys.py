#!/usr/bin/env python3
import asyncio
import nest_asyncio
import sys

nest_asyncio.apply()

sys.path.insert(0, 'src')
from sphero_sdk import SpheroRvrAsync, SerialAsyncDal

async def main():
    loop = asyncio.get_running_loop()
    dal = SerialAsyncDal(loop=loop, device="/dev/ttyS0", baud=115200)
    rvr = SpheroRvrAsync(dal=dal)

    try:
        await rvr.wake()
        await asyncio.sleep(2)

        print("Enabling color detection LED...")
        await rvr.enable_color_detection(is_enabled=True)
        await asyncio.sleep(0.2)

        print("Getting color values...")
        response = await rvr.get_rgbc_sensor_values()

        print(f"\nFull response dict: {response}")
        print(f"\nKeys in response: {list(response.keys())}")

        await rvr.enable_color_detection(is_enabled=False)
        await rvr.close()

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(main())
