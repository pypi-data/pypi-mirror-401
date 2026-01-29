#!/usr/bin/env python3
"""Move RVR forward 6 inches using MCP server tools."""

import asyncio

async def main():
    # Import the server components
    from sphero_rvr_mcp.server import connection_manager, initialize_server

    # Initialize server
    await initialize_server()

    # Connect to RVR
    print("Connecting to RVR...")
    result = await connection_manager.connect("/dev/ttyAMA0", 115200)
    print(f"Connect result: {result}")

    if not result.get("success"):
        print("Failed to connect!")
        return

    # Drive forward 6 inches = 0.1524 meters
    distance_meters = 6 * 0.0254  # 6 inches in meters
    print(f"Driving forward {distance_meters:.4f} meters (6 inches)...")

    if connection_manager.direct_serial and connection_manager.direct_serial.is_connected:
        ok = connection_manager.direct_serial.drive_forward_meters(distance_meters, 0.3)
        print(f"Drive result: success={ok}")
    else:
        print("Direct serial not connected!")

if __name__ == "__main__":
    asyncio.run(main())
