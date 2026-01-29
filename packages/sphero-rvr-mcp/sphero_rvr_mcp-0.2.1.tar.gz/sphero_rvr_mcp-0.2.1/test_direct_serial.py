#!/usr/bin/env python3
"""Quick test of direct serial protocol - run with RVR connected."""

import sys
import time
sys.path.insert(0, "src")

from sphero_rvr_mcp.protocol import DirectSerial

def main():
    port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyS0"

    print(f"Testing direct serial on {port}")
    ds = DirectSerial(port)

    if not ds.connect():
        print("Failed to connect!")
        return

    print("Connected. Waking RVR...")
    ds.wake()
    time.sleep(2)  # Give RVR time to wake up

    print("Testing commands...")

    # Test LEDs
    print("  LEDs red...")
    ds.set_all_leds(255, 0, 0)
    time.sleep(0.5)

    print("  LEDs green...")
    ds.set_all_leds(0, 255, 0)
    time.sleep(0.5)

    print("  LEDs blue...")
    ds.set_all_leds(0, 0, 255)
    time.sleep(0.5)

    print("  LEDs off...")
    ds.set_all_leds(0, 0, 0)

    # Test drive (very slow, short distance)
    print("  Drive forward slowly (speed=10, ~0.5s)...")
    ds.drive_with_heading(10, 0)
    time.sleep(0.5)
    ds.stop()

    print("Done!")
    ds.disconnect()


if __name__ == "__main__":
    main()
