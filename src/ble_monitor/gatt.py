from __future__ import annotations

from typing import Awaitable, Callable

from bleak import BleakClient


async def list_services(address: str) -> list[dict[str, object]]:
    """Connect to a BLE device and return its visible GATT services."""
    if not address.strip():
        raise ValueError("address must not be empty")

    async with BleakClient(address) as client:
        services = []
        for service in client.services:
            characteristics = []
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
    async with BleakClient(address) as client:
        return bytes(await client.read_gatt_char(characteristic_uuid))


async def write_characteristic(address: str, characteristic_uuid: str, value: bytes, response: bool = True) -> None:
    async with BleakClient(address) as client:
        await client.write_gatt_char(characteristic_uuid, value, response=response)


async def subscribe(address: str, characteristic_uuid: str, callback: Callable[[int, bytearray], None]) -> None:
    """Subscribe to notifications until the BLE session disconnects."""
    async with BleakClient(address) as client:
        await client.start_notify(characteristic_uuid, callback)
        await client.disconnect_event.wait()
        try:
            await client.stop_notify(characteristic_uuid)
        except Exception:
            pass
