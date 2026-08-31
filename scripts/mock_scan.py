from __future__ import annotations

import json

from ble_monitor.models import BLEDeviceRecord


MOCK_DEVICES = [
    BLEDeviceRecord(
        address="AA:BB:CC:DD:EE:01",
        name="Tarang-Sensor",
        rssi=-48,
        service_uuids=["180A"],
        metadata={"manufacturer": "demo"},
    ),
    BLEDeviceRecord(
        address="AA:BB:CC:DD:EE:02",
        name="BLE-Device-02",
        rssi=-67,
        service_uuids=["180F"],
        metadata={"manufacturer": "demo"},
    ),
]

for device in MOCK_DEVICES:
    print(json.dumps(device.model_dump(), default=str))
