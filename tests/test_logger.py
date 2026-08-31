import json

from ble_monitor.logger import EventLogger
from ble_monitor.models import BLEEvent


def test_event_logger_appends_jsonl(tmp_path):
    path = tmp_path / "events.jsonl"
    logger = EventLogger(path)
    logger.write(BLEEvent(event_type="device_discovered", address="AA:BB:CC:DD:EE:FF"))

    line = path.read_text(encoding="utf-8").strip()
    payload = json.loads(line)
    assert payload["event_type"] == "device_discovered"
