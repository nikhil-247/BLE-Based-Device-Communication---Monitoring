from __future__ import annotations

import asyncio
from collections.abc import Callable

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic


def _validate_text(value: str, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must not be empty")
    return value.strip()


async def list_services(address: str) -> list[dict[str, object]]:
    """Connect to a BLE device and return its visible GATT services."""
    device_address = _validate_text(address, "address")
    async with BleakClient(device_address) as client:
        services: list[dict[str, object]] = []
        for service in client.services:
            characteristics: list[dict[str, object]] = []
            for characteristic in service.characteristics:
                characteristics.append(
                    {
                        "uuid": characteristic.uuid,
                        "properties": list(characteristic.properties),
                    }
                )
            services.append(
                {
                    "uuid": service.uuid,
                    "description": service.description,
                    "characteristics": characteristics,
                }
            )
        return services


async def read_characteristic(address: str, characteristic_uuid: str) -> bytes:
    """Read bytes from a readable GATT characteristic."""
    device_address = _validate_text(address, "address")
    uuid = _validate_text(characteristic_uuid, "characteristic_uuid")
    async with BleakClient(device_address) as client:
        return bytes(await client.read_gatt_char(uuid))


async def write_characteristic(
    address: str,
    characteristic_uuid: str,
    value: bytes,
    response: bool = True,
) -> None:
    """Write bytes to a GATT characteristic."""
    device_address = _validate_text(address, "address")
    uuid = _validate_text(characteristic_uuid, "characteristic_uuid")
    if not isinstance(value, (bytes, bytearray, memoryview)):
        raise TypeError("value must be bytes-like")
    async with BleakClient(device_address) as client:
        await client.write_gatt_char(uuid, bytes(value), response=response)


async def subscribe(
    address: str,
    characteristic_uuid: str,
    callback: Callable[[BleakGATTCharacteristic, bytearray], None],
) -> None:
    """Subscribe to notifications until the device disconnects or task is cancelled."""
    device_address = _validate_text(address, "address")
    uuid = _validate_text(characteristic_uuid, "characteristic_uuid")
    disconnected = asyncio.Event()

    def on_disconnect(_client: BleakClient) -> None:
        disconnected.set()

    async with BleakClient(device_address, disconnected_callback=on_disconnect) as client:
        await client.start_notify(uuid, callback)
        try:
            await disconnected.wait()
        finally:
            if client.is_connected:
                await client.stop_notify(uuid)
