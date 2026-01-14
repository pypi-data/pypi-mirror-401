"""Simple Modbus RTU client tailored for half-duplex USB-serial adapters."""

from __future__ import annotations

from typing import List, Optional, Protocol

from .codec import ModbusFrame, ModbusProtocolError, build_frame, parse_frame


class TransactionalTransport(Protocol):
    """Protocol describing the minimal transport surface needed by the client."""

    def transact(
        self, payload: bytes, *, deadline: Optional[float] = None
    ) -> bytes: ...


class ModbusDeviceError(ModbusProtocolError):
    """Raised when the remote device reports a Modbus exception."""

    def __init__(self, function_code: int, exception_code: int) -> None:
        super().__init__(
            f"Remote unit returned exception 0x{exception_code:02X} for function 0x{function_code:02X}"
        )
        self.function_code = function_code
        self.exception_code = exception_code


class ModbusClient:
    """Blocking Modbus RTU client with a minimal API surface."""

    def __init__(self, transport: TransactionalTransport, unit_id: int = 1) -> None:
        if not 0 <= unit_id <= 247:
            raise ValueError("Unit ID must be between 0 and 247")
        self._transport = transport
        self._unit_id = unit_id

    def read_holding_registers(
        self,
        address: int,
        count: int,
        *,
        deadline: Optional[float] = None,
    ) -> List[int]:
        if not 0 <= address <= 0xFFFF:
            raise ValueError("Address must fit in 16 bits")
        if not 1 <= count <= 125:
            raise ValueError("Count must be between 1 and 125")
        payload = address.to_bytes(2, "big") + count.to_bytes(2, "big")
        frame = self._execute(0x03, payload, deadline=deadline)
        if not frame.payload:
            raise ModbusProtocolError("Missing byte count in response payload")
        byte_count = frame.payload[0]
        expected_bytes = count * 2
        if byte_count != expected_bytes:
            raise ModbusProtocolError(
                f"Expected {expected_bytes} data bytes, received {byte_count}"
            )
        data = frame.payload[1 : 1 + byte_count]
        if len(data) != expected_bytes:
            raise ModbusProtocolError("Response payload shorter than advertised")
        return [int.from_bytes(data[i : i + 2], "big") for i in range(0, len(data), 2)]

    def write_single_register(
        self,
        address: int,
        value: int,
        *,
        deadline: Optional[float] = None,
    ) -> None:
        if not 0 <= address <= 0xFFFF:
            raise ValueError("Address must fit in 16 bits")
        if not 0 <= value <= 0xFFFF:
            raise ValueError("Value must fit in 16 bits")
        payload = address.to_bytes(2, "big") + value.to_bytes(2, "big")
        frame = self._execute(0x06, payload, deadline=deadline)
        if frame.payload != payload:
            raise ModbusProtocolError("Write confirmation payload mismatch")

    def execute_raw(
        self,
        function_code: int,
        payload: bytes = b"",
        *,
        deadline: Optional[float] = None,
    ) -> bytes:
        """Send an arbitrary Modbus function and return the raw payload bytes."""

        frame = self._execute(function_code, payload, deadline=deadline)
        return frame.payload

    def _execute(
        self,
        function_code: int,
        payload: bytes,
        *,
        deadline: Optional[float] = None,
    ) -> ModbusFrame:
        request = build_frame(self._unit_id, function_code, payload)
        raw_response = self._transport.transact(request, deadline=deadline)
        response = parse_frame(raw_response)
        if response.unit_id not in (self._unit_id, 0):
            raise ModbusProtocolError(
                f"Unexpected unit {response.unit_id}; expected {self._unit_id} or broadcast echo"
            )
        if response.function_code & 0x80:
            code = response.payload[0] if response.payload else 0
            raise ModbusDeviceError(function_code, code)
        if response.function_code != function_code:
            raise ModbusProtocolError("Function code mismatch in response")
        return response
