from __future__ import annotations

from bleak import BleakScanner

from .models import BLEDeviceRecord


async def discover(timeout: float = 8.0) -> list[BLEDeviceRecord]:
    """Discover nearby BLE devices and normalize advertisement data."""
    if timeout <= 0:
        raise ValueError("timeout must be positive")

    discovered = await BleakScanner.discover(timeout=timeout, return_adv=True)
    records: list[BLEDeviceRecord] = []

    for address, pair in discovered.items():
        device, advertisement = pair
        records.append(
            BLEDeviceRecord(
                address=address,
                name=device.name or advertisement.local_name,
                rssi=advertisement.rssi,
                service_uuids=list(advertisement.service_uuids or []),
                metadata=dict(advertisement.manufacturer_data or {}),
            )
        )

    return sorted(records, key=lambda item: item.rssi if item.rssi is not None else -999, reverse=True)
