#!/usr/bin/env python3
import asyncio
import builtins
import nest_asyncio

# Apply nest_asyncio first
nest_asyncio.apply()

# Bypass firmware update prompt
builtins.input = lambda *args: ""

from sphero_sdk import SpheroRvrAsync, SerialAsyncDal

async def main():
    loop = asyncio.get_running_loop()
    dal = SerialAsyncDal(loop=loop, device='/dev/ttyS0', baud=115200)
    rvr = SpheroRvrAsync(dal=dal)
    
    try:
        print("🔌 Waking RVR...")
        await rvr.wake()
        await asyncio.sleep(2)

        print("🟠 Setting LEDs to ORANGE...")
        await rvr.set_all_leds(
            led_brightness=255,
            led_red=255,
            led_green=165,
            led_blue=0
        )
        
        print("✅ SUCCESS! RVR LEDs are now ORANGE! 🟠")
        await asyncio.sleep(2)

    finally:
        print("🔌 Closing connection...")
        await rvr.close()
        print("✅ Done!")

asyncio.run(main())
