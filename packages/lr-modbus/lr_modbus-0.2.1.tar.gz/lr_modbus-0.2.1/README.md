# lr-modbus

Lightweight Modbus RTU helpers tailored for FTDI-based hardware-in-the-loop setups. The package powers the CLI and automation utilities that ship with the UART<->RS-485 development board, but the components stand on their own and can be embedded into any Modbus RTU workflow.

## Features
- Blocking client with helpers for holding-register reads, single-register writes, and raw function dispatch
- Reference server with a thread-safe in-memory data model, optional listen-only mode, and deterministic shutdown hooks
- CRC-safe frame codec plus transactional serial transport tuned for half-duplex FTDI adapters
- Batteries-included CLI (`lr-modbus`) for quick experiments, scripting, and test automation

## Installation
```bash
python -m pip install lr-modbus
```

For development work inside this repository, install in editable mode together with the extra tooling:
```bash
python -m pip install -e python/lr_modbus[dev]
```

## Quick Start
### CLI
```bash
# Launch a server that seeds two holding registers and exits after 50 requests
lr-modbus --port /dev/ttyUSB0 server --holding 0=0x2A,1=0x1337 --max-requests 50

# Read two registers from another adapter
lr-modbus --port /dev/ttyUSB1 client --action read-holding --address 0 --count 2

# Write a single register
lr-modbus --port /dev/ttyUSB1 client --action write-single --address 5 --value 1234
```

The CLI targets the FT231XS + MAX1487CSA+ stack on the dev board, defaults to 115200-8N1, enforces Modbus RTU `t3.5` frame gaps, and gives each transaction a 2 s deadline. That means two adapters attached to the same host can verify their RS-485 link with no extra flags, while the `--timeout` option lets you shrink or grow the overall window. Common overrides include:

```bash
lr-modbus --port /dev/ttyUSB0 --baudrate 19200 --stopbits 1 --timeout 2 client --action read-holding --address 0 --count 4
```

Use `lr-modbus --help` for the full option matrix, including how to seed holding registers or stop the server after a fixed number of requests for HIL scripting.


### Library usage
```python
from lr_modbus import ModbusClient, ModbusServer, InMemoryDataModel
from lr_modbus.transport import SerialDeviceConfig, create_serial_transport

config = SerialDeviceConfig(port="/dev/ttyUSB0")
transport = create_serial_transport(config)
client = ModbusClient(transport, unit_id=1)

with transport:
    registers = client.read_holding_registers(0, 4)
    client.write_single_register(10, 0xBEEF)
```

To host a test server in the same script:
```python
data_model = InMemoryDataModel({0: 0x2A})
server = ModbusServer(transport, unit_id=1, data_model=data_model)
server.serve_forever(max_requests=10)
```

The transport exposes `transact()`, `read_frame()`, and `write_frame()` helpers for advanced use-cases such as bit-banging DE/RE GPIO hooks.


## Testing
```bash
make test
```

The target wires up `pytest` with coverage against the `lr_modbus` and `lr_dmx` packages. Tests rely on transport factories, so no physical hardware is required.

## Versioning & publishing
Package metadata lives in `python/lr_modbus/pyproject.toml` alongside the version marker in `python/lr_modbus/lr_modbus/__init__.py`. To publish a release from this repository root:
```bash
python -m pip install -e python/lr_modbus[dev]
python -m build python/lr_modbus -o dist/lr_modbus
python -m twine upload dist/lr_modbus/*
```


## License
Released under the MIT License. Copyright (c) 2026 LumenRadio AB.

```
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```


