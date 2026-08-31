from ble_monitor.models import BLEDeviceRecord, BLEEvent


def test_device_record_defaults():
    device = BLEDeviceRecord(address="AA:BB:CC:DD:EE:FF")
    assert device.address.endswith("FF")
    assert device.service_uuids == []


def test_event_serialization():
    event = BLEEvent(event_type="device_discovered", address="AA:BB:CC:DD:EE:FF")
    payload = event.model_dump(mode="json")
    assert payload["event_type"] == "device_discovered"
    assert payload["address"] == "AA:BB:CC:DD:EE:FF"
