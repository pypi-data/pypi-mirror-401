"""Helpers for encoding and decoding Modbus RTU frames."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

__all__ = [
    "ModbusFrame",
    "ModbusProtocolError",
    "ModbusFrameTooShort",
    "ModbusCrcError",
    "crc16",
    "build_frame",
    "build_exception_frame",
    "parse_frame",
]


@dataclass(frozen=True)
class ModbusFrame:
    """Container for a Modbus RTU frame without the CRC."""

    unit_id: int
    function_code: int
    payload: bytes


class ModbusProtocolError(RuntimeError):
    """Base class for protocol level issues."""


class ModbusFrameTooShort(ModbusProtocolError):
    """Raised when a frame does not contain enough bytes."""


class ModbusCrcError(ModbusProtocolError):
    """Raised when the CRC16 value is incorrect."""


_MIN_FRAME_LENGTH = 4  # address + function + crc(2) (+payload when present)


def crc16(payload: Iterable[int]) -> int:
    """Compute the Modbus RTU CRC16 for the given payload."""

    crc = 0xFFFF
    for byte in payload:
        crc ^= byte & 0xFF
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc & 0xFFFF


def _split(raw: bytes) -> tuple[bytes, int]:
    if len(raw) < _MIN_FRAME_LENGTH:
        raise ModbusFrameTooShort("Modbus RTU frame must be at least 4 bytes")
    payload, crc_bytes = raw[:-2], raw[-2:]
    return payload, int.from_bytes(crc_bytes, byteorder="little")


def build_frame(unit_id: int, function_code: int, payload: bytes = b"") -> bytes:
    if not 0 <= unit_id <= 247:
        raise ValueError("Unit ID must be between 0 and 247")
    data = bytes([unit_id & 0xFF, function_code & 0xFF]) + payload
    crc_value = crc16(data)
    return data + crc_value.to_bytes(2, byteorder="little")


def build_exception_frame(
    unit_id: int, function_code: int, exception_code: int
) -> bytes:
    payload = bytes([exception_code & 0xFF])
    return build_frame(unit_id, (function_code | 0x80) & 0xFF, payload)


def parse_frame(raw: bytes) -> ModbusFrame:
    payload, crc_value = _split(raw)
    calculated_crc = crc16(payload)
    if crc_value != calculated_crc:
        raise ModbusCrcError(
            f"CRC mismatch: expected 0x{crc_value:04X}, computed 0x{calculated_crc:04X}"
        )
    return ModbusFrame(
        unit_id=payload[0], function_code=payload[1], payload=payload[2:]
    )
