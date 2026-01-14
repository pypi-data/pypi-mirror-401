"""Hardware-facing transport helpers wrapping pyserial for half-duplex links."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Callable, Optional

import serial
from serial.serialutil import SerialBase

SerialHook = Optional[Callable[[], None]]


class SerialTransportError(RuntimeError):
    """Base class for transport layer failures."""


class SerialTimeoutError(SerialTransportError):
    """Raised when a frame is not available before the timeout elapses."""


@dataclass(frozen=True)
class SerialDeviceConfig:
    """Minimal serial configuration needed to talk to the FT231XS."""

    port: str
    baudrate: int = 115200
    bytesize: int = 8
    parity: str = "N"
    stopbits: float = 1.0
    timeout: float = 0.02
    write_timeout: float = 0.05
    inter_byte_timeout: float = 0.0

    def to_serial_kwargs(self) -> dict[str, object]:
        parity = {
            "N": serial.PARITY_NONE,
            "E": serial.PARITY_EVEN,
            "O": serial.PARITY_ODD,
            "M": serial.PARITY_MARK,
            "S": serial.PARITY_SPACE,
        }.get(self.parity.upper())
        if parity is None:
            raise ValueError("Parity must be one of N, E, O, M, S")

        stopbits = {
            1.0: serial.STOPBITS_ONE,
            1.5: serial.STOPBITS_ONE_POINT_FIVE,
            2.0: serial.STOPBITS_TWO,
        }.get(float(self.stopbits))
        if stopbits is None:
            raise ValueError("Stop bits must be 1, 1.5 or 2")

        bytesize = {
            5: serial.FIVEBITS,
            6: serial.SIXBITS,
            7: serial.SEVENBITS,
            8: serial.EIGHTBITS,
        }.get(int(self.bytesize))
        if bytesize is None:
            raise ValueError("Byte size must be between 5 and 8 bits")

        return {
            "port": self.port,
            "baudrate": self.baudrate,
            "bytesize": bytesize,
            "parity": parity,
            "stopbits": stopbits,
            "timeout": self.timeout,
            "write_timeout": self.write_timeout,
            "inter_byte_timeout": self.inter_byte_timeout,
        }


_FAST_T15 = 0.00075
_FAST_T35 = 0.00175


def _bits_per_character(config: SerialDeviceConfig) -> float:
    parity_bits = 0 if config.parity.upper() == "N" else 1
    return 1 + int(config.bytesize) + parity_bits + float(config.stopbits)


def _frame_gap_from_config(config: SerialDeviceConfig) -> float:
    if config.baudrate > 19200:
        return _FAST_T35
    bits_per_char = _bits_per_character(config)
    return 3.5 * (bits_per_char / config.baudrate)


def _start_timeout_from_config(config: SerialDeviceConfig) -> float:
    # Allow more time for slower baudrates; on faster links we can be stricter.
    if config.baudrate > 19200:
        return 0.1
    return 0.5


class SerialTransport:
    """Thin wrapper around pyserial that understands Modbus RTU framing."""

    def __init__(
        self,
        config: SerialDeviceConfig,
        *,
        frame_timeout: Optional[float] = None,
        start_timeout: Optional[float] = None,
        port_factory: Optional[Callable[..., serial.Serial]] = None,
        before_write: SerialHook = None,
        after_write: SerialHook = None,
    ) -> None:
        self._config = config
        derived_frame_timeout = _frame_gap_from_config(config)
        self._frame_timeout = (
            frame_timeout if frame_timeout is not None else derived_frame_timeout
        )
        derived_start_timeout = _start_timeout_from_config(config)
        self._start_timeout = (
            start_timeout if start_timeout is not None else derived_start_timeout
        )
        self._port_factory = port_factory or serial.Serial
        self._before_write = before_write
        self._after_write = after_write
        self._lock = threading.Lock()
        self._serial: Optional[SerialBase] = None

    def __enter__(self) -> "SerialTransport":
        self.open()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def open(self) -> None:
        if self._serial and self._serial.is_open:
            return
        self._serial = self._port_factory(**self._config.to_serial_kwargs())

    def close(self) -> None:
        if self._serial:
            self._serial.close()
            self._serial = None

    def write_frame(self, payload: bytes) -> None:
        self._ensure_open()
        if self._before_write:
            self._before_write()
        self._serial.reset_output_buffer()
        self._serial.write(payload)
        self._serial.flush()
        if self._after_write:
            self._after_write()

    def read_frame(self, *, deadline: Optional[float] = None) -> bytes:
        self._ensure_open()
        assert self._serial is not None  # type narrowing
        serial_port = self._serial
        buffer = bytearray()
        now = time.monotonic()
        default_start_deadline = now + self._start_timeout
        start_deadline = (
            min(deadline, default_start_deadline)
            if deadline is not None
            else default_start_deadline
        )
        frame_deadline: Optional[float] = None
        while True:
            self._check_deadline(deadline)
            byte = serial_port.read(1)
            if byte:
                buffer.extend(byte)
                now = time.monotonic()
                candidate_deadline = now + self._frame_timeout
                frame_deadline = (
                    min(deadline, candidate_deadline)
                    if deadline is not None
                    else candidate_deadline
                )
                continue
            now = time.monotonic()
            if not buffer:
                if now >= start_deadline:
                    raise SerialTimeoutError("Timed out waiting for frame start")
                continue
            if frame_deadline is not None and now >= frame_deadline:
                break
        if not buffer:
            raise SerialTimeoutError("Timed out waiting for complete frame")
        return bytes(buffer)

    def transact(self, payload: bytes, *, deadline: Optional[float] = None) -> bytes:
        with self._lock:
            self._ensure_open()
            self._check_deadline(deadline)
            assert self._serial is not None
            self._serial.reset_input_buffer()
            self.write_frame(payload)
            self._check_deadline(deadline)
            return self.read_frame(deadline=deadline)

    def _ensure_open(self) -> None:
        if not self._serial:
            raise SerialTransportError("Serial port has not been opened")

    @staticmethod
    def _check_deadline(deadline: Optional[float]) -> None:
        if deadline is not None and time.monotonic() >= deadline:
            raise SerialTimeoutError("Operation deadline expired")


def create_serial_transport(config: SerialDeviceConfig) -> SerialTransport:
    """Factory helper that can be patched in tests."""

    return SerialTransport(config)
