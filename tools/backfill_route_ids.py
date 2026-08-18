#!/usr/bin/env python3
"""Backfill stable ids into route and manual archive JSON files.

This migration keeps route-point identities stable even when titles change.
It also adds `fromId` / `toId` to manual route-leg geometry so leg matching can
prefer ids over titles.
"""

from __future__ import annotations

from collections import defaultdict, deque
from pathlib import Path
from typing import Any
import json
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
ROUTE_FILES = [
    ROOT / "docs" / "data" / "route.json",
    ROOT / "content" / "routes" / "route-so-far.json",
]
GEOMETRY_FILE = ROOT / "content" / "routes" / "voyage-geometry.json"
MANUAL_DIRS = [
    ROOT / "admin-input",
    ROOT / "data" / "ais" / "manual",
]


def load_json(path: Path, fallback: Any):
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def normalise_text(value: Any) -> str:
    text = unicodedata.normalize("NFKD", str(value or "")).encode("ascii", "ignore").decode("ascii")
    text = "".join(ch.lower() if ch.isalnum() else " " for ch in text)
    return " ".join(text.split())


def point_title(point: dict[str, Any]) -> str:
    return str(point.get("title") or point.get("name") or "").strip()


def point_key(point: dict[str, Any]) -> tuple[str, ...]:
    date = normalise_text(point.get("date"))
    title = normalise_text(point_title(point))
    lat = point.get("lat")
    lng = point.get("lng")
    coords = ()
    if lat is not None and lng is not None:
        try:
            coords = (f"{float(lat):.6f}", f"{float(lng):.6f}")
        except Exception:
            coords = ()
    return (date, title, *coords)


def date_coord_key(point: dict[str, Any]) -> tuple[str, ...]:
    date = normalise_text(point.get("date"))
    lat = point.get("lat")
    lng = point.get("lng")
    if lat is None or lng is None:
        return ()
    try:
        return (date, f"{float(lat):.6f}", f"{float(lng):.6f}")
    except Exception:
        return ()


def assign_ids(route: list[dict[str, Any]], prefix: str = "route") -> dict[tuple[str, ...], deque[str]]:
    used_ids: set[str] = set()
    highest_seq = 0
    for point in route:
        raw_id = str(point.get("id") or "").strip()
        if raw_id:
            point["id"] = raw_id
            used_ids.add(raw_id)
            if raw_id.startswith(f"{prefix}-"):
                suffix = raw_id[len(prefix) + 1 :]
                if suffix.isdigit():
                    highest_seq = max(highest_seq, int(suffix))

    next_seq = highest_seq + 1 if highest_seq else 1
    for point in route:
        if str(point.get("id") or "").strip():
            continue
        while True:
            candidate = f"{prefix}-{next_seq:03d}"
            next_seq += 1
            if candidate not in used_ids:
                point["id"] = candidate
                used_ids.add(candidate)
                break

    buckets: dict[tuple[str, ...], deque[str]] = defaultdict(deque)
    for point in route:
        pid = str(point.get("id") or "").strip()
        if not pid:
            continue
        buckets[point_key(point)].append(pid)
        dc_key = date_coord_key(point)
        if dc_key:
            buckets[dc_key].append(pid)
        title_key = (normalise_text(point.get("date")), normalise_text(point.get("name") or point.get("title")))
        buckets[title_key].append(pid)
    return buckets


def lookup_id(point: dict[str, Any], buckets: dict[tuple[str, ...], deque[str]]) -> str | None:
    candidates = [
        point_key(point),
        date_coord_key(point),
        (normalise_text(point.get("date")), normalise_text(point.get("name") or point.get("title"))),
        (normalise_text(point.get("date")), normalise_text(point.get("title") or point.get("name"))),
    ]
    for key in candidates:
        queue = buckets.get(key)
        if queue:
            return queue.popleft()
    return None


def backfill_route_file(path: Path) -> dict[tuple[str, ...], deque[str]]:
    route = load_json(path, [])
    if not isinstance(route, list):
        raise SystemExit(f"{path} must contain a JSON list")
    buckets = assign_ids(route, "route")
    save_json(path, route)
    return buckets


def backfill_geometry_file(path: Path, route: list[dict[str, Any]]) -> int:
    data = load_json(path, {"schemaVersion": 1, "legs": []})
    if not isinstance(data, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    route_by_index = route
    route_by_key = {
        (normalise_text(point.get("date")), normalise_text(point_title(point))): point.get("id")
        for point in route_by_index
        if point.get("id")
    }
    updated = 0
    for leg in data.get("legs", []):
        if not isinstance(leg, dict):
            continue
        from_id = None
        to_id = None
        if isinstance(leg.get("fromIndex"), int) and isinstance(leg.get("toIndex"), int):
            fi = leg["fromIndex"]
            ti = leg["toIndex"]
            if 0 <= fi < len(route_by_index):
                from_id = route_by_index[fi].get("id")
            if 0 <= ti < len(route_by_index):
                to_id = route_by_index[ti].get("id")
        if not from_id and leg.get("fromDate") and leg.get("fromTitle"):
            from_id = route_by_key.get((normalise_text(leg["fromDate"]), normalise_text(leg["fromTitle"])))
        if not to_id and leg.get("toDate") and leg.get("toTitle"):
            to_id = route_by_key.get((normalise_text(leg["toDate"]), normalise_text(leg["toTitle"])))
        if from_id and leg.get("fromId") != from_id:
            leg["fromId"] = from_id
            updated += 1
        if to_id and leg.get("toId") != to_id:
            leg["toId"] = to_id
            updated += 1
    save_json(path, data)
    return updated


def backfill_manual_archives(route_buckets: dict[tuple[str, ...], deque[str]]) -> list[Path]:
    updated_paths: list[Path] = []
    for directory in MANUAL_DIRS:
        if not directory.exists():
            continue
        for path in sorted(directory.glob("*.json")):
            data = load_json(path, None)
            if not isinstance(data, dict):
                continue
            route_point = data.get("routePoint")
            if not isinstance(route_point, dict):
                continue
            route_id = lookup_id(route_point, route_buckets)
            if not route_id:
                continue
            if route_point.get("id") == route_id:
                continue
            route_point["id"] = route_id
            tracker = data.get("tracker")
            if isinstance(tracker, dict) and not tracker.get("routePointId"):
                tracker["routePointId"] = route_id
            save_json(path, data)
            updated_paths.append(path)
    return updated_paths


def main() -> None:
    route_buckets = {}
    docs_route = load_json(ROUTE_FILES[0], [])
    if not isinstance(docs_route, list):
        raise SystemExit(f"{ROUTE_FILES[0]} must contain a JSON list")
    route_buckets = assign_ids(docs_route, "route")
    save_json(ROUTE_FILES[0], docs_route)

    for path in ROUTE_FILES[1:]:
        route = load_json(path, [])
        if not isinstance(route, list):
            raise SystemExit(f"{path} must contain a JSON list")
        assign_ids(route, "route")
        save_json(path, route)

    geometry_updates = backfill_geometry_file(GEOMETRY_FILE, docs_route)
    manual_updates = backfill_manual_archives(route_buckets)

    print(f"Updated route files: {', '.join(str(p.relative_to(ROOT)) for p in ROUTE_FILES)}")
    print(f"Updated geometry file: {GEOMETRY_FILE.relative_to(ROOT)} ({geometry_updates} id fields)")
    print(f"Updated manual archives: {len(manual_updates)} file(s)")
    for path in manual_updates[:25]:
        print(f"- {path.relative_to(ROOT)}")
    if len(manual_updates) > 25:
        print(f"- ... and {len(manual_updates) - 25} more")


if __name__ == "__main__":
    main()
