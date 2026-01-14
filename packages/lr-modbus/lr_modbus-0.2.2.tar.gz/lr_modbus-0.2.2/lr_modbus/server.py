"""Reference Modbus RTU server with a pluggable data model."""

from __future__ import annotations

import logging
import threading
from typing import Callable, Dict, List, Optional, Protocol

from .codec import (
    ModbusProtocolError,
    build_exception_frame,
    build_frame,
    parse_frame,
)
from .transport import SerialTimeoutError

_LOG = logging.getLogger(__name__)


class RegisterDataModel(Protocol):
    def read_holding_registers(self, address: int, count: int) -> List[int]: ...

    def write_single_register(self, address: int, value: int) -> None: ...


class InMemoryDataModel(RegisterDataModel):
    """Thread-safe backing store for holding registers."""

    def __init__(self, initial: Optional[Dict[int, int]] = None) -> None:
        self._values: Dict[int, int] = dict(initial or {})
        self._lock = threading.Lock()

    def read_holding_registers(self, address: int, count: int) -> List[int]:
        with self._lock:
            return [self._values.get(address + offset, 0) for offset in range(count)]

    def write_single_register(self, address: int, value: int) -> None:
        with self._lock:
            self._values[address] = value & 0xFFFF


class ModbusServer:
    """Blocking Modbus RTU server designed for HIL test automation."""

    def __init__(
        self,
        transport,
        *,
        unit_id: int = 1,
        data_model: Optional[RegisterDataModel] = None,
        listen_only: bool = False,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        if not 0 <= unit_id <= 247:
            raise ValueError("Unit ID must be between 0 and 247")
        self._transport = transport
        self._unit_id = unit_id
        self._model = data_model or InMemoryDataModel()
        self._listen_only = listen_only
        self._logger = logger or _LOG

    def serve_forever(
        self,
        *,
        should_stop: Optional[Callable[[], bool]] = None,
        max_requests: Optional[int] = None,
    ) -> None:
        processed = 0
        with self._transport:
            while True:
                if should_stop and should_stop():
                    break
                try:
                    raw = self._transport.read_frame()
                except SerialTimeoutError:
                    continue
                response = self.handle_raw_frame(raw)
                if response and not self._listen_only:
                    try:
                        self._transport.write_frame(response)
                    except SerialTimeoutError as exc:
                        self._logger.warning("Failed to transmit response: %s", exc)
                if response is not None:
                    processed += 1
                    if max_requests and processed >= max_requests:
                        break

    def handle_raw_frame(self, raw: bytes) -> Optional[bytes]:
        try:
            frame = parse_frame(raw)
        except ModbusProtocolError as exc:
            self._logger.debug("Dropping malformed frame: %s", exc)
            return None

        if frame.unit_id == 0:
            self._logger.debug(
                "Broadcast frame received: function 0x%02X", frame.function_code
            )
            self._process_broadcast(frame)
            return None

        if frame.unit_id != self._unit_id:
            return None

        if self._listen_only:
            self._logger.info("Listen-only frame: %s", frame)
            return None

        return self._build_response(frame)

    def _process_broadcast(self, frame) -> None:
        if frame.function_code == 0x06 and len(frame.payload) == 4:
            address = int.from_bytes(frame.payload[0:2], "big")
            value = int.from_bytes(frame.payload[2:4], "big")
            self._model.write_single_register(address, value)

    def _build_response(self, frame) -> Optional[bytes]:
        try:
            if frame.function_code == 0x03 and len(frame.payload) >= 4:
                start = self._decode_u16(frame.payload[:2])
                count = self._decode_u16(frame.payload[2:4])
                registers = self._model.read_holding_registers(start, count)
                byte_count = len(registers) * 2
                payload = bytes([byte_count]) + b"".join(
                    value.to_bytes(2, "big") for value in registers
                )
                self._log_transaction(
                    "read",
                    address=start,
                    count=count,
                    data=registers,
                    function=frame.function_code,
                )
                return build_frame(self._unit_id, frame.function_code, payload)
            if frame.function_code == 0x06 and len(frame.payload) == 4:
                address = self._decode_u16(frame.payload[:2])
                value = self._decode_u16(frame.payload[2:4])
                self._model.write_single_register(address, value)
                self._log_transaction(
                    "write",
                    address=address,
                    count=1,
                    data=[value],
                    function=frame.function_code,
                )
                return build_frame(self._unit_id, frame.function_code, frame.payload)
        except Exception as exc:  # pragma: no cover - extremely rare defensive path
            self._logger.exception("Unhandled server error", exc_info=exc)
            return build_exception_frame(self._unit_id, frame.function_code, 0x04)

        return build_exception_frame(self._unit_id, frame.function_code, 0x01)

    @staticmethod
    def _decode_u16(data: bytes) -> int:
        if len(data) != 2:
            raise ModbusProtocolError("Expected 2 byte value in payload")
        return int.from_bytes(data, "big")

    def _log_transaction(
        self,
        operation: str,
        *,
        address: int,
        count: int,
        data: List[int],
        function: int,
    ) -> None:
        if not self._logger.isEnabledFor(logging.INFO):
            return
        if operation == "read":
            self._logger.info(
                "Unit %d FC=0x%02X read holding[%d..%d] -> %s",
                self._unit_id,
                function,
                address,
                address + max(count - 1, 0),
                data,
            )
        elif operation == "write":
            self._logger.info(
                "Unit %d FC=0x%02X write holding[%d] := %s",
                self._unit_id,
                function,
                address,
                data[0] if data else None,
            )
