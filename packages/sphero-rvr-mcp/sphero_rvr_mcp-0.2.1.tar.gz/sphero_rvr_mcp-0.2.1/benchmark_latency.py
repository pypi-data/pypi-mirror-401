#!/usr/bin/env python3
"""Benchmark script to measure SDK vs direct serial latency for RVR commands.

This script measures:
1. SDK path latency (current implementation)
2. Direct serial path latency (new implementation)

Run with RVR connected and powered on.
"""

import asyncio
import time
import statistics
import sys

# SDK imports
from sphero_sdk import SpheroRvrAsync
from sphero_sdk.asyncio.client.dal.serial_async_dal import SerialAsyncDal

# Direct serial imports
import serial
import struct


# =============================================================================
# Protocol Constants (from SDK source)
# =============================================================================
SOP = 0x8D  # Start of packet
EOP = 0xD8  # End of packet
ESC = 0xAB  # Escape byte
ESC_SOP = 0x05  # Escaped start
ESC_EOP = 0x50  # Escaped end
ESC_ESC = 0x23  # Escaped escape

# Device IDs
DID_DRIVE = 0x16

# Command IDs
CID_DRIVE_WITH_HEADING = 0x07
CID_RAW_MOTORS = 0x01

# Flags
FLAG_HAS_TARGET = 0x10
FLAG_HAS_SOURCE = 0x20
FLAG_REQUEST_RESPONSE = 0x02

# Target addresses
TARGET_MCU = 0x02  # Drive commands go to MCU
SOURCE_HOST = 0x00  # We're the host


# =============================================================================
# Direct Serial Protocol Implementation
# =============================================================================

def checksum(data: bytes) -> int:
    """Calculate checksum: sum of bytes AND 0xFF, then XOR 0xFF."""
    return (sum(data) & 0xFF) ^ 0xFF


def escape_byte(b: int) -> bytes:
    """Escape special bytes."""
    if b == SOP:
        return bytes([ESC, ESC_SOP])
    elif b == EOP:
        return bytes([ESC, ESC_EOP])
    elif b == ESC:
        return bytes([ESC, ESC_ESC])
    else:
        return bytes([b])


def escape_buffer(data: bytes) -> bytes:
    """Escape all special bytes in buffer."""
    result = bytearray()
    for b in data:
        result.extend(escape_byte(b))
    return bytes(result)


def build_packet(did: int, cid: int, target: int, seq: int, data: bytes = b"",
                 request_response: bool = False) -> bytes:
    """Build a complete RVR packet.

    Packet structure:
    - SOP (1 byte)
    - Escaped content:
      - Flags (1 byte)
      - Target (1 byte, if FLAG_HAS_TARGET)
      - Source (1 byte, if FLAG_HAS_SOURCE)
      - DID (1 byte)
      - CID (1 byte)
      - SEQ (1 byte)
      - Data (variable)
      - Checksum (1 byte)
    - EOP (1 byte)
    """
    flags = FLAG_HAS_TARGET | FLAG_HAS_SOURCE
    if request_response:
        flags |= FLAG_REQUEST_RESPONSE

    # Build header + body (unescaped)
    header = bytes([flags, target, SOURCE_HOST, did, cid, seq])
    content = header + data
    chk = checksum(content)
    content_with_chk = content + bytes([chk])

    # Escape and wrap
    escaped = escape_buffer(content_with_chk)
    return bytes([SOP]) + escaped + bytes([EOP])


def build_drive_with_heading(speed: int, heading: int, flags: int = 0, seq: int = 0) -> bytes:
    """Build drive_with_heading command packet.

    Args:
        speed: 0-255
        heading: 0-359 degrees
        flags: 0=forward, 1=reverse
        seq: sequence number
    """
    # Pack data: speed (uint8), heading (uint16 big-endian), flags (uint8)
    data = struct.pack(">BHB", speed, heading, flags)
    return build_packet(DID_DRIVE, CID_DRIVE_WITH_HEADING, TARGET_MCU, seq, data)


def build_stop(seq: int = 0) -> bytes:
    """Build stop command (drive with speed=0)."""
    return build_drive_with_heading(0, 0, 0, seq)


# =============================================================================
# Benchmark Functions
# =============================================================================

async def benchmark_sdk_latency(rvr, iterations: int = 20) -> list:
    """Measure SDK drive_with_heading latency."""
    latencies = []

    for i in range(iterations):
        start = time.perf_counter()
        await rvr.drive_with_heading(0, 0, 0)  # Stop command
        elapsed = (time.perf_counter() - start) * 1000  # ms
        latencies.append(elapsed)
        await asyncio.sleep(0.05)  # Small delay between commands

    return latencies


def benchmark_direct_latency(port: str, iterations: int = 20) -> list:
    """Measure direct serial latency (fire-and-forget, no response wait)."""
    latencies = []

    ser = serial.Serial(port, 115200, timeout=0.1)
    try:
        for i in range(iterations):
            packet = build_stop(seq=i % 256)

            start = time.perf_counter()
            ser.write(packet)
            ser.flush()  # Ensure data is sent
            elapsed = (time.perf_counter() - start) * 1000  # ms

            latencies.append(elapsed)
            time.sleep(0.05)
    finally:
        ser.close()

    return latencies


def benchmark_direct_with_response(port: str, iterations: int = 20) -> list:
    """Measure direct serial latency including response wait."""
    latencies = []

    ser = serial.Serial(port, 115200, timeout=0.5)
    try:
        for i in range(iterations):
            # Build packet that requests response
            flags = FLAG_HAS_TARGET | FLAG_HAS_SOURCE | FLAG_REQUEST_RESPONSE
            data = struct.pack(">BHB", 0, 0, 0)  # stop command
            header = bytes([flags, TARGET_MCU, SOURCE_HOST, DID_DRIVE, CID_DRIVE_WITH_HEADING, i % 256])
            content = header + data
            chk = checksum(content)
            content_with_chk = content + bytes([chk])
            escaped = escape_buffer(content_with_chk)
            packet = bytes([SOP]) + escaped + bytes([EOP])

            start = time.perf_counter()
            ser.write(packet)
            ser.flush()

            # Wait for response (look for EOP)
            response = b""
            while True:
                b = ser.read(1)
                if not b:
                    break  # timeout
                response += b
                if b[0] == EOP:
                    break

            elapsed = (time.perf_counter() - start) * 1000  # ms
            latencies.append(elapsed)
            time.sleep(0.05)
    finally:
        ser.close()

    return latencies


def print_stats(name: str, latencies: list):
    """Print latency statistics."""
    if not latencies:
        print(f"{name}: No data")
        return

    print(f"\n{name}:")
    print(f"  Samples:    {len(latencies)}")
    print(f"  Min:        {min(latencies):.2f} ms")
    print(f"  Max:        {max(latencies):.2f} ms")
    print(f"  Mean:       {statistics.mean(latencies):.2f} ms")
    print(f"  Median:     {statistics.median(latencies):.2f} ms")
    if len(latencies) > 1:
        print(f"  Std Dev:    {statistics.stdev(latencies):.2f} ms")


async def main():
    port = "/dev/ttyS0"
    iterations = 20

    if len(sys.argv) > 1:
        port = sys.argv[1]
    if len(sys.argv) > 2:
        iterations = int(sys.argv[2])

    print(f"RVR Latency Benchmark")
    print(f"=====================")
    print(f"Port: {port}")
    print(f"Iterations: {iterations}")

    # First test direct serial (doesn't require SDK initialization)
    print("\n--- Testing Direct Serial (fire-and-forget) ---")
    try:
        direct_ff_latencies = benchmark_direct_latency(port, iterations)
        print_stats("Direct Serial (no response)", direct_ff_latencies)
    except Exception as e:
        print(f"Direct serial test failed: {e}")
        direct_ff_latencies = []

    print("\n--- Testing Direct Serial (with response) ---")
    try:
        direct_resp_latencies = benchmark_direct_with_response(port, iterations)
        print_stats("Direct Serial (with response)", direct_resp_latencies)
    except Exception as e:
        print(f"Direct serial with response test failed: {e}")
        direct_resp_latencies = []

    # Now test SDK
    print("\n--- Testing SDK Path ---")
    print("Initializing SDK (this may take a few seconds)...")

    try:
        loop = asyncio.get_event_loop()
        dal = SerialAsyncDal(loop, port, 115200)
        rvr = SpheroRvrAsync(dal)

        await rvr.wake()
        await asyncio.sleep(2)  # Wait for RVR to be ready

        sdk_latencies = await benchmark_sdk_latency(rvr, iterations)
        print_stats("SDK Path", sdk_latencies)

        await rvr.close()
    except Exception as e:
        print(f"SDK test failed: {e}")
        sdk_latencies = []

    # Summary comparison
    print("\n" + "=" * 50)
    print("SUMMARY COMPARISON")
    print("=" * 50)

    if direct_ff_latencies:
        print(f"Direct (fire-and-forget): {statistics.mean(direct_ff_latencies):.2f} ms avg")
    if direct_resp_latencies:
        print(f"Direct (with response):   {statistics.mean(direct_resp_latencies):.2f} ms avg")
    if sdk_latencies:
        print(f"SDK Path:                 {statistics.mean(sdk_latencies):.2f} ms avg")

    if sdk_latencies and direct_ff_latencies:
        speedup = statistics.mean(sdk_latencies) / statistics.mean(direct_ff_latencies)
        print(f"\nPotential speedup (fire-and-forget): {speedup:.1f}x faster")

    if sdk_latencies and direct_resp_latencies:
        speedup = statistics.mean(sdk_latencies) / statistics.mean(direct_resp_latencies)
        print(f"Potential speedup (with response):   {speedup:.1f}x faster")


if __name__ == "__main__":
    asyncio.run(main())
