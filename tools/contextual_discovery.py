#!/usr/bin/env python3
"""Validate and publish the curated Contextual Discovery layer.

This tool deliberately does not search the web. Research is curated and source-backed
in content/discoveries/contextual-discoveries.json; the tool applies the agreed
proximity rules, matches discoveries to route stops, and writes public JSON.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import argparse
import json
import math

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "content" / "discoveries" / "contextual-discoveries.json"
ROUTE = ROOT / "docs" / "data" / "route.json"
OUTPUT = ROOT / "docs" / "data" / "discoveries.json"
JOURNAL = ROOT / "docs" / "data" / "journal.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def normalise(value: str | None) -> str:
    return " ".join(str(value or "").casefold().replace("–", "-").replace("—", "-").split())


def haversine_metres(a: tuple[float, float], b: tuple[float, float]) -> int:
    radius = 6_371_000
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return int(round(2 * radius * math.asin(math.sqrt(h))))


def stop_title(stop: dict) -> str:
    return str(stop.get("title") or stop.get("name") or "")


def threshold_for(stop: dict, policy: dict) -> int:
    status = normalise(stop.get("status"))
    if status == "moored":
        return int(policy["mooredRadiusMetres"])
    if status == "at anchor":
        return int(policy["anchoredRadiusMetres"])
    if status == "underway" and not policy.get("underwayAutomaticSearch", False):
        return 0
    return int(policy["anchoredRadiusMetres"])


def distance_band(distance: int | None, contextual_area: bool) -> str:
    if contextual_area:
        return "contextual"
    if distance is None:
        return "editorial"
    if distance <= 250:
        return "gold"
    if distance <= 500:
        return "silver"
    return "bronze"


def qualify(discovery: dict, stop: dict, policy: dict) -> tuple[bool, str, int | None]:
    contextual_area = bool(discovery.get("contextualArea"))
    distance = discovery.get("distanceMetres")
    feature = discovery.get("featureLocation")
    if isinstance(feature, dict) and all(k in feature for k in ("lat", "lng")):
        distance = haversine_metres(
            (float(stop["lat"]), float(stop["lng"])),
            (float(feature["lat"]), float(feature["lng"])),
        )
    distance = int(distance) if distance is not None else None

    evidence = set(discovery.get("evidence") or [])
    overrides = set(policy.get("evidenceOverrides") or [])
    has_override = bool(evidence & overrides)
    exceptional = bool(discovery.get("exceptional"))
    normal_limit = threshold_for(stop, policy)
    exceptional_limit = int(policy["exceptionalRadiusMetres"])

    if contextual_area:
        return True, "place-defining context", distance
    if distance is None:
        return False, "missing distance or contextual-area flag", distance
    if normal_limit and distance <= normal_limit:
        return True, f"within {normal_limit} m {normalise(stop.get('status')) or 'stop'} radius", distance
    if distance <= exceptional_limit and exceptional and has_override:
        return True, "exceptional discovery admitted by evidence override", distance
    return False, f"outside discovery policy ({distance} m)", distance


def build(check_only: bool = False) -> dict:
    source = load_json(SOURCE)
    route = load_json(ROUTE)
    journal = load_json(JOURNAL)
    journal_ids = {str(e.get("id")) for e in journal.get("entries", []) if e.get("id")} if isinstance(journal, dict) else set()
    policy = source["policy"]
    route_by_title = {normalise(stop_title(stop)): (i, stop) for i, stop in enumerate(route)}
    errors: list[str] = []
    published: list[dict] = []

    for item in source.get("discoveries", []):
        if not item.get("approved"):
            continue
        key = normalise(item.get("routeStopTitle"))
        if key not in route_by_title:
            errors.append(f"{item.get('id')}: route stop not found: {item.get('routeStopTitle')}")
            continue
        index, stop = route_by_title[key]
        ok, qualification, distance = qualify(item, stop, policy)
        if not ok:
            errors.append(f"{item.get('id')}: {qualification}")
            continue
        journal_entry_id = item.get("journalEntryId")
        if journal_entry_id and str(journal_entry_id) not in journal_ids:
            errors.append(f"{item.get('id')}: journal entry not found: {journal_entry_id}")
            continue
        source_info = item.get("source") or {}
        if not source_info.get("title") or not str(source_info.get("url", "")).startswith("https://"):
            errors.append(f"{item.get('id')}: source title and HTTPS URL are required")
            continue
        public = {k: v for k, v in item.items() if k not in {"approved"}}
        public.update(
            {
                "routeStopIndex": index,
                "routeStopDate": stop.get("date"),
                "routeStopStatus": stop.get("status") or ("Current position" if stop.get("phase") == "current" else "Voyage stop"),
                "distanceMetres": distance,
                "distanceBand": distance_band(distance, bool(item.get("contextualArea"))),
                "qualification": qualification,
            }
        )
        published.append(public)

    ids = [d.get("id") for d in published]
    if len(ids) != len(set(ids)):
        errors.append("duplicate discovery IDs")
    entries = [d.get("journalEntryId") for d in published if d.get("journalEntryId")]
    if len(entries) != len(set(entries)):
        errors.append("more than one approved discovery targets the same journal entry")

    if errors:
        raise SystemExit("Contextual Discovery validation failed:\n- " + "\n- ".join(errors))

    result = {
        "schemaVersion": source.get("schemaVersion", 1),
        "release": "Contextual Discovery",
        "generatedUtc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "principle": source.get("principle"),
        "policy": policy,
        "count": len(published),
        "discoveries": published,
    }
    if not check_only:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and publish Contextual Discovery data")
    parser.add_argument("--check", action="store_true", help="validate without writing docs/data/discoveries.json")
    args = parser.parse_args()
    result = build(check_only=args.check)
    print(f"Contextual Discovery: {result['count']} approved discoveries")
    if args.check:
        print("Validation only; public JSON was not changed.")
    else:
        print(f"Wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
