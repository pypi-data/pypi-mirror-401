#!/usr/bin/env python3
"""Test drive_to_position_si command directly."""

import serial
import time
import struct

# Protocol constants
SOP = 0x8D
EOP = 0xD8
ESC = 0xAB
ESC_SOP = 0x05
ESC_EOP = 0x50
ESC_ESC = 0x23

# Device IDs
DID_DRIVE = 0x16
DID_SENSOR = 0x18
DID_POWER = 0x13

# Command IDs
CID_WAKE = 0x0D
CID_RESET_YAW = 0x06
CID_RESET_LOCATOR = 0x13
CID_SET_LOCATOR_FLAGS = 0x17
CID_DRIVE_TO_POSITION_SI = 0x38
CID_DRIVE_WITH_HEADING = 0x07

# Targets
TARGET_MCU = 0x02  # Drive, sensors (ST processor)
TARGET_BT = 0x01   # LEDs, Bluetooth (Nordic processor)
SOURCE_HOST = 0x00

# Flags
FLAG_HAS_TARGET = 0x10
FLAG_HAS_SOURCE = 0x20


def checksum(data: bytes) -> int:
    return (sum(data) & 0xFF) ^ 0xFF


def escape_buffer(data: bytes) -> bytes:
    result = bytearray()
    for b in data:
        if b == SOP:
            result.extend([ESC, ESC_SOP])
        elif b == EOP:
            result.extend([ESC, ESC_EOP])
        elif b == ESC:
            result.extend([ESC, ESC_ESC])
        else:
            result.append(b)
    return bytes(result)


_seq = 0

def next_seq() -> int:
    global _seq
    _seq = (_seq + 1) & 0xFF
    return _seq


def build_packet(did: int, cid: int, target: int, data: bytes = b"") -> bytes:
    flags = FLAG_HAS_TARGET | FLAG_HAS_SOURCE
    seq = next_seq()
    header = bytes([flags, target, SOURCE_HOST, did, cid, seq])
    content = header + data
    content_with_chk = content + bytes([checksum(content)])
    return bytes([SOP]) + escape_buffer(content_with_chk) + bytes([EOP])


def build_simple_packet(did: int, cid: int, data: bytes = b"") -> bytes:
    """Build packet with FLAGS=0x06 (no target/source, error-only response)."""
    FLAGS = 0x06
    seq = next_seq()
    content = bytes([FLAGS, did, cid, seq]) + data
    chksum = (~(sum(content) % 256)) & 0xFF
    return bytes([SOP]) + escape_buffer(content + bytes([chksum])) + bytes([EOP])


def send_and_print(ser, name, packet):
    print(f"\n{name}:")
    print(f"  Packet: {packet.hex()}")
    ser.write(packet)
    ser.flush()
    time.sleep(0.1)
    # Read any response
    if ser.in_waiting:
        resp = ser.read(ser.in_waiting)
        print(f"  Response: {resp.hex()}")


def main():
    port = "/dev/ttyAMA0"
    baud = 115200

    print(f"Connecting to {port} at {baud} baud...")
    ser = serial.Serial(port, baud, timeout=0.1)
    time.sleep(0.5)

    # Wake
    wake_pkt = build_packet(DID_POWER, CID_WAKE, TARGET_BT)
    send_and_print(ser, "WAKE", wake_pkt)
    time.sleep(1)

    # Reset yaw (use simple packet format)
    reset_yaw_pkt = build_simple_packet(DID_DRIVE, CID_RESET_YAW, b'')
    send_and_print(ser, "RESET_YAW", reset_yaw_pkt)
    time.sleep(0.2)

    # Set locator flags (0 = no auto-calibrate, for manual control)
    set_flags_pkt = build_simple_packet(DID_SENSOR, CID_SET_LOCATOR_FLAGS, bytes([0x00]))
    send_and_print(ser, "SET_LOCATOR_FLAGS (0)", set_flags_pkt)
    time.sleep(0.2)

    # Reset locator (use simple packet format with DID_SENSOR)
    reset_loc_pkt = build_simple_packet(DID_SENSOR, CID_RESET_LOCATOR, b'')
    send_and_print(ser, "RESET_LOCATOR", reset_loc_pkt)
    time.sleep(0.2)

    # Drive to position: 6 inches forward = 0.1524 meters
    # Use the corrected packet format (FLAGS=0x06, no target/source)
    distance = 0.1524  # 6 inches in meters
    speed = 0.3  # slow speed
    yaw = 0.0
    x = 0.0
    y = distance
    flags_byte = 0

    # Build packet with simplified format matching CircuitPython SDK
    FLAGS = 0x06  # No target/source, error-only response
    seq = next_seq()
    data = struct.pack(">ffffB", yaw, x, y, speed, flags_byte)
    content = bytes([FLAGS, DID_DRIVE, CID_DRIVE_TO_POSITION_SI, seq]) + data
    chksum = (~(sum(content) % 256)) & 0xFF
    drive_pkt = bytes([SOP]) + escape_buffer(content + bytes([chksum])) + bytes([EOP])

    send_and_print(ser, f"DRIVE_TO_POSITION_SI (y={y}, speed={speed})", drive_pkt)

    print("\nWaiting 3 seconds for movement...")
    time.sleep(3)

    # Check for any responses
    if ser.in_waiting:
        resp = ser.read(ser.in_waiting)
        print(f"Final response: {resp.hex()}")

    ser.close()
    print("\nDone.")


if __name__ == "__main__":
    main()
