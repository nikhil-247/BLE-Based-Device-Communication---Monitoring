from __future__ import annotations

import argparse
import asyncio
import json

from .gatt import list_services
from .logger import EventLogger
from .models import BLEEvent
from .scanner import discover


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="BLE Device Communication & Monitoring")
    sub = parser.add_subparsers(dest="command", required=True)

    scan = sub.add_parser("scan", help="Discover nearby BLE devices")
    scan.add_argument("--timeout", type=float, default=8.0)
    scan.add_argument("--log", type=str, default=None)

    services = sub.add_parser("services", help="Inspect GATT services and characteristics")
    services.add_argument("--address", required=True)
    return parser


async def run(args: argparse.Namespace) -> None:
    if args.command == "scan":
        logger = EventLogger(args.log) if args.log else None
        records = await discover(args.timeout)
        for record in records:
            print(json.dumps(record.model_dump(), default=str))
            if logger:
                logger.write(
                    BLEEvent(
                        event_type="device_discovered",
                        address=record.address,
                        name=record.name,
                        rssi=record.rssi,
                        details={"service_uuids": record.service_uuids},
                    )
                )
    elif args.command == "services":
        result = await list_services(args.address)
        print(json.dumps(result, indent=2))


def main() -> None:
    args = build_parser().parse_args()
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
