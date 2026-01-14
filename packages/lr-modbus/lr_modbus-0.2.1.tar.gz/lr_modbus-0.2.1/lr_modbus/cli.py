"""Command line tooling for the lr_modbus package."""

from __future__ import annotations

import argparse
import logging
import sys
import time
from typing import Callable, Dict, Optional

from .client import ModbusClient
from .server import InMemoryDataModel, ModbusServer
from .transport import SerialDeviceConfig, SerialTransportError, create_serial_transport

_LOG = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a Modbus RTU client or server over FTDI USB."
    )
    parser.add_argument(
        "--port", required=True, help="Serial device path, e.g. /dev/ttyUSB0"
    )
    parser.add_argument(
        "--baudrate", type=int, default=115200, help="Serial baudrate (default: 115200)"
    )
    parser.add_argument("--parity", choices=["N", "E", "O", "M", "S"], default="N")
    parser.add_argument("--stopbits", type=float, default=1.0)
    parser.add_argument("--bytesize", type=int, default=8)
    parser.add_argument(
        "--timeout",
        type=float,
        default=2.0,
        help="Maximum duration of the Modbus operation in seconds (0 = wait indefinitely)",
    )
    parser.add_argument("--unit-id", type=int, default=1, help="Modbus unit identifier")
    parser.add_argument(
        "--log-level", default="INFO", help="Python logging level (default: INFO)"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    client = subparsers.add_parser("client", help="Perform a single Modbus transaction")
    client.add_argument(
        "--action",
        choices=["read-holding", "write-single"],
        default="read-holding",
        help="Client action to perform",
    )
    client.add_argument("--address", type=int, default=0, help="Register address")
    client.add_argument(
        "--count", type=int, default=1, help="Number of registers when reading"
    )
    client.add_argument(
        "--value", type=int, default=0, help="Value to use for write-single"
    )

    server = subparsers.add_parser(
        "server", help="Start a Modbus RTU server or listener"
    )
    server.add_argument(
        "--listen-only", action="store_true", help="Do not reply, just log frames"
    )
    server.add_argument(
        "--holding",
        default="",
        help="Comma separated register initialisation, e.g. 0=10,5=0x20",
    )
    server.add_argument(
        "--max-requests",
        type=int,
        default=0,
        help="Stop after N handled frames (0 = run forever)",
    )
    server.add_argument(
        "--stop-after",
        type=float,
        default=0.0,
        help="Stop after N seconds (0 = run until interrupted)",
    )

    return parser


def parse_holding_initialisation(raw: str) -> Dict[int, int]:
    registers: Dict[int, int] = {}
    if not raw:
        return registers
    for item in raw.split(","):
        if not item.strip():
            continue
        if "=" not in item:
            raise argparse.ArgumentTypeError(f"Invalid register expression: {item}")
        key, value = item.split("=", 1)
        address = int(key.strip(), 0)
        registers[address] = int(value.strip(), 0) & 0xFFFF
    return registers


def _deadline_condition(duration: float) -> Optional[Callable[[], bool]]:
    if duration <= 0:
        return None
    deadline = time.monotonic() + duration
    return lambda: time.monotonic() >= deadline


def _operation_deadline(duration: float) -> Optional[float]:
    if duration <= 0:
        return None
    return time.monotonic() + duration


def run_cli(argv: Optional[list[str]] = None, transport_factory=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.INFO))

    config = SerialDeviceConfig(
        port=args.port,
        baudrate=args.baudrate,
        parity=args.parity,
        stopbits=args.stopbits,
        bytesize=args.bytesize,
    )

    factory = transport_factory or create_serial_transport

    try:
        if args.command == "client":
            return _run_client(args, config, factory)
        if args.command == "server":
            return _run_server(args, config, factory)
        parser.error("No command specified")
    except SerialTransportError as exc:
        _LOG.error("Serial error: %s", exc)
        return 2
    except KeyboardInterrupt:
        _LOG.info("Interrupted")
        return 130
    return 0


def _run_client(args, config, factory) -> int:
    transport = factory(config)
    client = ModbusClient(transport, unit_id=args.unit_id)
    with transport:
        deadline = _operation_deadline(args.timeout)
        if args.action == "read-holding":
            values = client.read_holding_registers(
                args.address,
                args.count,
                deadline=deadline,
            )
            for offset, value in enumerate(values):
                absolute = args.address + offset
                print(f"holding[{absolute}] = {value}")
        else:
            client.write_single_register(
                args.address,
                args.value,
                deadline=deadline,
            )
            print(
                f"holding[{args.address}] := {args.value}"  # noqa: T201 - CLI feedback
            )
    return 0


def _run_server(args, config, factory) -> int:
    initial = parse_holding_initialisation(args.holding)
    transport = factory(config)
    data_model = InMemoryDataModel(initial)
    server = ModbusServer(
        transport,
        unit_id=args.unit_id,
        data_model=data_model,
        listen_only=args.listen_only,
    )
    stop = _deadline_condition(args.stop_after)
    max_req = args.max_requests if args.max_requests > 0 else None
    server.serve_forever(should_stop=stop, max_requests=max_req)
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    return run_cli(argv)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
