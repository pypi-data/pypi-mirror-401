"""Lightweight Modbus RTU helpers for FTDI based hardware-in-the-loop setups."""

from .client import ModbusClient, ModbusDeviceError
from .server import InMemoryDataModel, ModbusServer
from .transport import (
    SerialDeviceConfig,
    SerialTimeoutError,
    SerialTransport,
    SerialTransportError,
)
from .codec import ModbusFrame, ModbusProtocolError

__all__ = [
    "InMemoryDataModel",
    "ModbusClient",
    "ModbusDeviceError",
    "ModbusFrame",
    "ModbusProtocolError",
    "ModbusServer",
    "SerialDeviceConfig",
    "SerialTimeoutError",
    "SerialTransport",
    "SerialTransportError",
]

__version__ = "0.1.2"
