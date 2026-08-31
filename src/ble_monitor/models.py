from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class BLEDeviceRecord(BaseModel):
    model_config = ConfigDict(extra="allow")

    address: str
    name: str | None = None
    rssi: int | None = Field(default=None, ge=-127, le=20)
    service_uuids: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class BLEEvent(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    event_type: str
    address: str
    name: str | None = None
    rssi: int | None = None
    details: dict[str, Any] = Field(default_factory=dict)
