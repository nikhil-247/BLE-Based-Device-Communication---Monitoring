# BLE Device Communication & Monitoring

A Python-based Bluetooth Low Energy (BLE) monitoring toolkit for discovering nearby devices, inspecting advertised services, tracking connection state, and recording device telemetry in a structured format.

## Highlights

- BLE device discovery with RSSI and advertisement metadata
- Service and characteristic inspection for compatible GATT devices
- Connection-state monitoring with reconnect handling
- Read, write and notification helpers for GATT characteristics
- JSONL event logging for repeatable analysis
- Hardware-free mock mode for development and CI
- Type hints, validation, tests and packaging

## Architecture

```text
BLE Adapter / Mock Source
          |
          v
     Device Scanner
          |
          v
   Device Normalization
          |
    +-----+------+
    |            |
    v            v
GATT Session   Event Logger
    |            |
    v            v
Services &     JSONL Logs
Characteristics
```

## Project structure

```text
BLE-Based-Device-Communication---Monitoring/
├── src/ble_monitor/
│   ├── __init__.py
│   ├── models.py
│   ├── scanner.py
│   ├── gatt.py
│   ├── logger.py
│   └── cli.py
├── scripts/
│   └── mock_scan.py
├── tests/
│   ├── test_models.py
│   └── test_logger.py
├── logs/
│   └── .gitkeep
├── .github/workflows/ci.yml
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10+
- BLE-capable adapter for real discovery
- Windows, Linux or macOS with Bluetooth permissions

The project uses [Bleak](https://github.com/hbldh/bleak) for cross-platform BLE access.

## Setup

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
pip install -e .
```

## Scan for nearby devices

```bash
python -m ble_monitor.cli scan --timeout 8
```

For environments without a BLE adapter:

```bash
python scripts/mock_scan.py
```

## Inspect GATT services

```bash
python -m ble_monitor.cli services --address AA:BB:CC:DD:EE:FF
```

## Log discovery events

```bash
python -m ble_monitor.cli scan --timeout 8 --log logs/discovery.jsonl
```

## Development

```bash
pytest -q
```

CI runs the test suite on supported Python versions.

## Safety and privacy

Use this project only with devices you own or are authorized to inspect. BLE advertisements can contain identifiers and other metadata. Do not commit captured logs containing personal or sensitive information. Sample/mock data is synthetic.

## Limitations

BLE discovery behavior varies by operating system and adapter. Some platforms expose different advertisement fields and require additional permissions. GATT operations also depend on the target device's available services and characteristic properties.

## License

MIT
