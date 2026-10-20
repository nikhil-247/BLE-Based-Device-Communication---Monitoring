import pytest

from bleak.backends.characteristic import BleakGATTCharacteristic

from ble_monitor import gatt


@pytest.mark.parametrize(
    ("call", "args"),
    [
        (gatt.list_services, ("",)),
        (gatt.read_characteristic, ("", "2A37")),
        (gatt.read_characteristic, ("AA:BB:CC:DD:EE:FF", "")),
        (gatt.write_characteristic, ("AA:BB:CC:DD:EE:FF", "", b"x")),
        (gatt.subscribe, ("AA:BB:CC:DD:EE:FF", "", lambda *_: None)),
    ],
)
@pytest.mark.asyncio
async def test_gatt_helpers_reject_empty_required_values(call, args):
    with pytest.raises(ValueError):
        await call(*args)


@pytest.mark.asyncio
async def test_write_rejects_non_bytes_payload():
    with pytest.raises(TypeError, match="bytes-like"):
        await gatt.write_characteristic("AA:BB:CC:DD:EE:FF", "2A37", "not bytes")  # type: ignore[arg-type]


class FakeCharacteristic:
    uuid = "00002a37-0000-1000-8000-00805f9b34fb"
    properties = ["read", "notify"]


class FakeService:
    uuid = "0000180d-0000-1000-8000-00805f9b34fb"
    description = "Heart Rate"
    characteristics = [FakeCharacteristic()]


class FakeClient:
    def __init__(self, address, disconnected_callback=None):
        self.address = address
        self.disconnected_callback = disconnected_callback
        self.services = [FakeService()]
        self.is_connected = True
        self.read_uuid = None
        self.write_payload = None
        self.notify_callback = None
        self.stopped_uuid = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args):
        return False

    async def read_gatt_char(self, uuid):
        self.read_uuid = uuid
        return bytearray([1, 2, 3])

    async def write_gatt_char(self, uuid, value, response=True):
        self.write_payload = (uuid, value, response)

    async def start_notify(self, uuid, callback):
        self.notify_callback = (uuid, callback)
        # Trigger the disconnect event in this fake client so the test doesn't wait.
        if self.disconnected_callback:
            self.disconnected_callback(self)

    async def stop_notify(self, uuid):
        self.stopped_uuid = uuid


@pytest.mark.asyncio
async def test_list_services_serializes_visible_characteristics(monkeypatch):
    monkeypatch.setattr(gatt, "BleakClient", FakeClient)

    result = await gatt.list_services("AA:BB:CC:DD:EE:FF")

    assert result[0]["description"] == "Heart Rate"
    assert result[0]["characteristics"][0]["properties"] == ["read", "notify"]


@pytest.mark.asyncio
async def test_read_returns_bytes(monkeypatch):
    monkeypatch.setattr(gatt, "BleakClient", FakeClient)

    result = await gatt.read_characteristic("AA:BB:CC:DD:EE:FF", "2A37")

    assert result == b"\x01\x02\x03"


@pytest.mark.asyncio
async def test_write_sends_bytes_and_response_flag(monkeypatch):
    client = FakeClient("AA:BB:CC:DD:EE:FF")
    monkeypatch.setattr(gatt, "BleakClient", lambda *_a, **_k: client)

    await gatt.write_characteristic("AA:BB:CC:DD:EE:FF", "2A37", bytearray([4, 5]), response=False)

    assert client.write_payload == ("2A37", b"\x04\x05", False)


@pytest.mark.asyncio
async def test_subscribe_uses_disconnect_callback_and_cleans_up(monkeypatch):
    client = FakeClient("AA:BB:CC:DD:EE:FF")
    monkeypatch.setattr(gatt, "BleakClient", lambda *_a, **_k: client)
    observed = []

    await gatt.subscribe(
        "AA:BB:CC:DD:EE:FF",
        "2A37",
        lambda characteristic, data: observed.append((characteristic, data)),
    )

    assert client.notify_callback is not None
    assert client.stopped_uuid == "2A37"
