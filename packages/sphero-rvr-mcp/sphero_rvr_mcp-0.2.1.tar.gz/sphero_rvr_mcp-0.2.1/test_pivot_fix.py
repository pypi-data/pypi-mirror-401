#!/usr/bin/env python3
"""Hardware test script for pivot fix verification.

This script tests the firmware-based pivot implementation to verify:
1. 90-degree pivots (left and right)
2. 180-degree pivot
3. Multiple consecutive pivots

Usage:
    python test_pivot_fix.py
"""

import asyncio
import sys

# Add src to path
sys.path.insert(0, '/home/jsperson/source/sphero_rvr_mcp/src')

from sphero_rvr_mcp.api import RVRClient


async def test_pivot_accuracy():
    """Test pivot accuracy with firmware-based approach."""

    client = RVRClient(log_level="INFO")

    try:
        print("=" * 60)
        print("Pivot Accuracy Test - Firmware-Based Approach")
        print("=" * 60)
        print()

        # Initialize and connect
        print("Initializing RVR client...")
        await client.initialize()

        print("Connecting to RVR...")
        result = await client.connect()
        if not result["success"]:
            print(f"❌ Connection failed: {result.get('error')}")
            return

        print(f"✓ Connected: {result['message']}")
        print()

        # Turn LEDs orange to indicate test mode
        await client.set_all_leds(255, 165, 0)
        await asyncio.sleep(0.5)

        # Test 1: Pivot 90° left
        print("Test 1: Pivot 90° LEFT")
        print("-" * 40)
        input("  Place RVR in starting position. Press ENTER to start...")

        result = await client._movement_service.pivot(degrees=-90)

        if result["success"]:
            print(f"  ✓ Pivot completed")
            print(f"    Rotation time: {result.get('rotation_time', 'N/A')}s")
            input("  Measure actual rotation. Press ENTER to continue...")
        else:
            print(f"  ❌ Pivot failed: {result.get('error')}")

        print()

        # Reset for next test
        await asyncio.sleep(2)

        # Test 2: Pivot 90° right
        print("Test 2: Pivot 90° RIGHT")
        print("-" * 40)
        input("  Place RVR in starting position. Press ENTER to start...")

        result = await client._movement_service.pivot(degrees=90)

        if result["success"]:
            print(f"  ✓ Pivot completed")
            print(f"    Rotation time: {result.get('rotation_time', 'N/A')}s")
            input("  Measure actual rotation. Press ENTER to continue...")
        else:
            print(f"  ❌ Pivot failed: {result.get('error')}")

        print()

        # Reset for next test
        await asyncio.sleep(2)

        # Test 3: Pivot 180°
        print("Test 3: Pivot 180°")
        print("-" * 40)
        input("  Place RVR in starting position. Press ENTER to start...")

        result = await client._movement_service.pivot(degrees=180)

        if result["success"]:
            print(f"  ✓ Pivot completed")
            print(f"    Rotation time: {result.get('rotation_time', 'N/A')}s")
            input("  Measure actual rotation. Press ENTER to continue...")
        else:
            print(f"  ❌ Pivot failed: {result.get('error')}")

        print()

        # Test 4: Multiple consecutive pivots
        print("Test 4: Consecutive 90° pivots (4x left = full rotation)")
        print("-" * 40)
        input("  Place RVR in starting position. Press ENTER to start...")

        for i in range(4):
            print(f"  Pivot {i+1}/4...")
            result = await client._movement_service.pivot(degrees=-90)
            if not result["success"]:
                print(f"  ❌ Pivot {i+1} failed: {result.get('error')}")
                break
            await asyncio.sleep(1)
        else:
            print(f"  ✓ All 4 pivots completed")
            input("  RVR should be back at starting orientation. Press ENTER...")

        print()

        # Turn LEDs green to indicate test complete
        await client.set_all_leds(0, 255, 0)
        await asyncio.sleep(1)
        await client.turn_leds_off()

        print("=" * 60)
        print("Test Complete!")
        print()
        print("Expected Results:")
        print("  ✓ Pivots should be within ±5° of target")
        print("  ✓ No over-rotation (e.g., 340° when expecting 90°)")
        print("  ✓ Consistent behavior across multiple pivots")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\nCleaning up...")
        await client.shutdown()
        print("Done.")


if __name__ == "__main__":
    asyncio.run(test_pivot_accuracy())
