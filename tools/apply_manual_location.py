#!/usr/bin/env python3
"""Apply a manually selected Juno's 7 location to route/dashboard data.

Commit 1 of Geographic Intelligence:
- performs a server-side reverse lookup at publish time;
- stores the returned metadata alongside the new route point and tracker data;
- keeps existing site behaviour backwards-compatible because the original name/date/lat/lng fields remain unchanged.
"""

from __future__ import annotations

from pathlib import Path
import json
import sys
import time

from geo_lookup import reverse_lookup

ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.1.1"
RELEASE = "Geographic Intelligence polish"

def configure_console() -> None:
    """Avoid Windows cp1252 crashes if lookup text contains accented characters."""
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def backup(path: Path) -> None:
    if path.exists():
        path.with_suffix(path.suffix + ".bak-geo-1").write_text(
            path.read_text(encoding="utf-8"),
            encoding="utf-8",
        )


def enrich_update(data: dict) -> dict:
    route_point = data["routePoint"]
    lat = route_point.get("lat")
    lng = route_point.get("lng")
    fallback = route_point.get("name") or data.get("tracker", {}).get("area") or "Manual location"

    if lat is not None and lng is not None:
        location = reverse_lookup(lat, lng, fallback)
        route_point["location"] = location
        tracker = data.setdefault("tracker", {})
        tracker["location"] = location
        tracker["area"] = location.get("displayName") or fallback
        time.sleep(1)

    return data


def load_update(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if "routePoint" not in data or "tracker" not in data:
        raise SystemExit("Invalid manual location update.")
    data["routePoint"]["phase"] = "current"
    return enrich_update(data)


def normalise_route(route: list, new_point: dict) -> list:
    cleaned = []
    for item in route:
        if item.get("name") == new_point.get("name") and item.get("date") == new_point.get("date"):
            continue
        if item.get("phase") == "current":
            item["phase"] = "onboard"
        cleaned.append(item)
    new_point["phase"] = "current"
    cleaned.append(new_point)
    return cleaned


def update_route(path: Path, point: dict) -> bool:
    if not path.exists():
        return False
    route = normalise_route(json.loads(path.read_text(encoding="utf-8")), point)
    backup(path)
    path.write_text(json.dumps(route, indent=2, ensure_ascii=False), encoding="utf-8")
    return True


def update_dashboard(path: Path, update: dict) -> bool:
    if not path.exists():
        return False

    data = json.loads(path.read_text(encoding="utf-8"))
    data["version"] = VERSION
    data["release"] = RELEASE

    manual = update["tracker"]
    pos = manual["position"]
    location = manual.get("location") or update["routePoint"].get("location") or {}
    display = location.get("displayName") or manual.get("area") or update["routePoint"].get("name", "Manual location")

    tracker = data.setdefault("tracker", {})
    tracker["workflow"] = tracker.get("workflow", "running")
    tracker["provider"] = "manual / provider not configured"
    tracker["liveAis"] = False
    tracker["lastManualLookupUtc"] = manual["timestampUtc"]
    tracker["latestStatus"] = f"Manual location: {display}"
    tracker["latestLocationName"] = update["routePoint"].get("name")
    tracker["latestFriendlyLocation"] = display
    tracker["location"] = location
    tracker["latestSource"] = manual.get("source", "captains dashboard")
    tracker["latestPrecisePosition"] = pos if "precise" in pos.get("precision", "") else None
    tracker["latestApproximatePosition"] = pos
    tracker["note"] = update["routePoint"].get("note", "")

    backup(path)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return True


def update_version(path: Path) -> None:
    if not path.exists():
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        data = {}
    data["version"] = VERSION
    data["release"] = RELEASE
    backup(path)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_record(update: dict) -> Path:
    ts = update["tracker"]["timestampUtc"].replace(":", "").replace("-", "")
    name = update["routePoint"]["name"].lower().replace(" ", "-").replace("/", "-")
    out = ROOT / "data" / "ais" / "manual" / f"{ts[:8]}-{name}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(update, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


def main() -> None:
    configure_console()

    if len(sys.argv) != 2:
        raise SystemExit("Usage: python tools/apply_manual_location.py admin-input/latest-location.json")

    update = load_update(Path(sys.argv[1]))
    changed = []

    for rel in ["site/data/route.json", "content/routes/route-so-far.json", "docs/data/route.json"]:
        if update_route(ROOT / rel, update["routePoint"]):
            changed.append(rel)

    for rel in ["site/data/dashboard.json", "docs/data/dashboard.json"]:
        if update_dashboard(ROOT / rel, update):
            changed.append(rel)

    update_version(ROOT / "site/data/version.json")
    update_version(ROOT / "docs/data/version.json")
    (ROOT / "VERSION").write_text(VERSION + "\n", encoding="utf-8")
    record = write_record(update)

    route_path = ROOT / "site/data/route.json"
    if route_path.exists():
        count = sum(
            1
            for p in json.loads(route_path.read_text(encoding="utf-8"))
            if p.get("phase") == "current"
        )
        if count != 1:
            raise SystemExit(f"Expected exactly one current marker, found {count}.")

    loc = update["routePoint"].get("location", {})
    print("Manual location applied.")
    print(f"Location: {update['routePoint']['name']}")
    print(f"Friendly location: {loc.get('displayName', update['routePoint']['name'])}")
    print(f"Coordinates: {update['routePoint']['lat']}, {update['routePoint']['lng']}")
    print(f"Tracker record: {record.relative_to(ROOT)}")
    print("Updated files where present:")
    for item in changed:
        print(f"- {item}")


if __name__ == "__main__":
    main()
