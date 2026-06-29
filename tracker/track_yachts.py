#!/usr/bin/env python3
"""
Juno's 7 tracker scaffold.

This script is intentionally provider-neutral.

It writes stable output files for the journal, but it will not pretend to have live AIS data
until a real data source is configured.

Outputs:
  data/ais/latest/<vessel>.json
  data/ais/archive/YYYY-MM-DD.jsonl
  site/data/tracker.json

To connect a provider:
  - implement fetch_position_for_vessel()
  - or provide data via an API endpoint / GitHub secret
"""

from pathlib import Path
from datetime import datetime, timezone
import json
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "tracker" / "config.json"
LATEST_DIR = ROOT / "data" / "ais" / "latest"
ARCHIVE_DIR = ROOT / "data" / "ais" / "archive"
SITE_TRACKER = ROOT / "site" / "data" / "tracker.json"

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))

def fetch_position_for_vessel(vessel: dict) -> dict | None:
    """
    Provider hook.

    Return a dict like:

    {
      "timestampUtc": "2026-06-29T17:00:00+00:00",
      "latitude": 38.43164,
      "longitude": 20.58843,
      "speedKnots": 0.0,
      "courseDegrees": 0,
      "status": "At anchor",
      "destination": null,
      "source": "configured-provider"
    }

    Current default returns None because no live AIS provider has been configured.
    """
    provider = os.getenv("AIS_PROVIDER", "").strip().lower()

    if not provider:
        return None

    # Future providers can be added here.
    # Example:
    # if provider == "my_api":
    #     return fetch_from_my_api(vessel)

    return None

def write_latest(vessel: dict, position: dict | None) -> dict:
    LATEST_DIR.mkdir(parents=True, exist_ok=True)

    if position:
        payload = {
            "vesselKey": vessel["key"],
            "displayName": vessel["displayName"],
            "journalName": vessel.get("journalName"),
            "mmsi": vessel["mmsi"],
            "imo": vessel.get("imo"),
            "role": vessel.get("role"),
            "lastUpdatedUtc": utc_now_iso(),
            "status": "live",
            "message": "Live position retrieved.",
            "position": position,
            "source": position.get("source")
        }
    else:
        payload = {
            "vesselKey": vessel["key"],
            "displayName": vessel["displayName"],
            "journalName": vessel.get("journalName"),
            "mmsi": vessel["mmsi"],
            "imo": vessel.get("imo"),
            "role": vessel.get("role"),
            "lastUpdatedUtc": utc_now_iso(),
            "status": "not_configured",
            "message": "Tracker ran, but no live AIS provider has been configured.",
            "position": None,
            "source": None
        }

    out = LATEST_DIR / f"{vessel['key']}.json"
    old = out.read_text(encoding="utf-8") if out.exists() else None
    new = json.dumps(payload, indent=2)
    out.write_text(new, encoding="utf-8")
    return payload

def append_archive(payloads: list[dict]) -> None:
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    archive_file = ARCHIVE_DIR / f"{day}.jsonl"

    with archive_file.open("a", encoding="utf-8") as f:
        for payload in payloads:
            f.write(json.dumps(payload, separators=(",", ":")) + "\n")

def write_site_tracker(config: dict, payloads: list[dict]) -> None:
    SITE_TRACKER.parent.mkdir(parents=True, exist_ok=True)

    site_payload = {
        "lastTrackerRunUtc": utc_now_iso(),
        "status": "live" if any(p["status"] == "live" for p in payloads) else "not_configured",
        "provider": config.get("source", {}).get("provider"),
        "vessels": payloads,
        "note": "Live tracking requires an AIS data source to be configured." if not any(p["status"] == "live" for p in payloads) else None
    }

    SITE_TRACKER.write_text(json.dumps(site_payload, indent=2), encoding="utf-8")

def main() -> int:
    config = load_config()
    payloads = []

    for vessel in config["vessels"]:
        if not vessel.get("enabled", True):
            continue

        position = fetch_position_for_vessel(vessel)
        payloads.append(write_latest(vessel, position))

    append_archive(payloads)
    write_site_tracker(config, payloads)

    if any(p["status"] == "live" for p in payloads):
        print("Tracker ran with live data.")
    else:
        print("Tracker ran. No AIS provider configured yet.")

    return 0

if __name__ == "__main__":
    sys.exit(main())
