#!/usr/bin/env python3
"""Geographic lookup helpers for Juno's 7 Journal.

This module is deliberately used only by the local publishing tools. The static
GitHub Pages site should never call public geocoding services from a visitor's
browser.
"""

from __future__ import annotations

from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json
import math
import time
from typing import Any

NOMINATIM_URL = "https://nominatim.openstreetmap.org/reverse"
USER_AGENT = "Junos7Journal/2.2-feature local-publishing-tool"
LOOKUP_PROVIDER = "OpenStreetMap Nominatim"

# Small English normalisation table for the Greek places we are currently using.
# Nominatim sometimes returns local-language names even when Accept-Language is set.
NAME_TRANSLATIONS = {
    "Ελλάς": "Greece",
    "Ελλάδα": "Greece",
    "Περιφέρεια Ιονίων Νήσων": "Ionian Islands",
    "Περιφέρεια Νοτίου Αιγαίου": "South Aegean",
    "Περιφερειακή Ενότητα Κέρκυρας": "Corfu regional unit",
    "Κέρκυρα": "Corfu Town",
    "Δήμος Κεντρικής Κέρκυρας και Διαποντίων Νήσων": "Central Corfu and Diapontia Islands",
}

# Lightweight island inference for the current voyage area. This is intentionally
# conservative: it only fills an island when coordinates are clearly in the area.
ISLAND_AREAS = [
    ("Corfu", 39.35, 39.85, 19.55, 20.15),
    ("Paxos", 39.12, 39.30, 20.08, 20.28),
    ("Kefalonia", 38.05, 38.50, 20.30, 20.85),
    ("Ithaca", 38.30, 38.55, 20.55, 20.85),
    ("Zakynthos", 37.55, 37.95, 20.55, 21.10),
    ("Kos", 36.70, 37.05, 26.90, 27.45),
    ("Rhodes", 35.85, 36.50, 27.60, 28.35),
    ("Symi", 36.50, 36.75, 27.70, 28.00),
    ("Chalki", 36.15, 36.32, 27.50, 27.72),
    ("Nisyros", 36.52, 36.70, 27.05, 27.25),
    ("Lipsi", 37.25, 37.35, 26.70, 26.85),
    ("Patmos", 37.25, 37.40, 26.45, 26.65),
    ("Amorgos", 36.75, 36.95, 25.70, 26.05),
    ("Ios", 36.65, 36.80, 25.20, 25.40),
]


def english(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    return NAME_TRANSLATIONS.get(value, value)


def nice_join(parts) -> str:
    output = []
    for part in parts:
        part = english(part)
        if part and part not in output:
            output.append(part)
    return ", ".join(output)


def infer_island(lat: float, lng: float) -> str | None:
    for name, min_lat, max_lat, min_lng, max_lng in ISLAND_AREAS:
        if min_lat <= lat <= max_lat and min_lng <= lng <= max_lng:
            return name
    return None


def reverse_lookup_raw(lat: float, lng: float, zoom: int) -> dict:
    params = urlencode(
        {
            "format": "jsonv2",
            "lat": f"{lat:.6f}",
            "lon": f"{lng:.6f}",
            "zoom": zoom,
            "addressdetails": 1,
            "namedetails": 1,
        }
    )
    request = Request(
        f"{NOMINATIM_URL}?{params}",
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "Accept-Language": "en",
        },
    )
    with urlopen(request, timeout=12) as response:
        return json.loads(response.read().decode("utf-8"))


def build_location(raw: dict, lat: float, lng: float, fallback_name: str) -> dict:
    address = raw.get("address", {}) or {}
    country = english(address.get("country"))
    country_code = (address.get("country_code") or "").upper() or None
    region = english(address.get("state") or address.get("region"))
    county = english(address.get("county"))
    municipality = english(address.get("municipality") or address.get("city") or address.get("town"))
    island = english(address.get("island")) or infer_island(lat, lng)

    nearest_place = english(
        address.get("city")
        or address.get("town")
        or address.get("village")
        or address.get("hamlet")
        or address.get("municipality")
        or address.get("county")
    )
    local_area = english(address.get("suburb") or address.get("neighbourhood") or address.get("quarter"))

    # Avoid unhelpful duplication such as "Near Corfu Town, Corfu Town".
    place_for_display = nearest_place
    if place_for_display and island and place_for_display.lower() == island.lower():
        place_for_display = None

    if island and place_for_display:
        display = f"{island}, near {place_for_display}"
    elif island:
        display = island
    elif place_for_display:
        display = f"Near {place_for_display}"
    else:
        display = fallback_name

    suffix = nice_join([region if region not in {island, nearest_place} else None, country])
    if suffix and suffix not in display:
        display = f"{display}, {suffix}"

    short_name = nice_join([local_area, nearest_place, island or municipality or county]) or fallback_name

    return {
        "lookupStatus": "ok",
        "lookupProvider": LOOKUP_PROVIDER,
        "osmType": raw.get("osm_type"),
        "osmId": raw.get("osm_id"),
        "displayName": display,
        "shortName": short_name,
        "rawDisplayName": raw.get("display_name"),
        "country": country,
        "countryCode": country_code,
        "region": region,
        "county": county,
        "municipality": municipality,
        "island": island,
        "nearestPlace": nearest_place,
        "localArea": local_area,
    }


def reverse_lookup(lat, lng, fallback_name: str = "Manual location") -> dict:
    """Return normalised English location metadata for a lat/lng."""
    latitude = float(lat)
    longitude = float(lng)

    try:
        # A slightly more detailed first pass usually gives better coastal place
        # names than zoom=10. If it fails to produce useful admin data, fall back.
        raw = reverse_lookup_raw(latitude, longitude, zoom=14)
        location = build_location(raw, latitude, longitude, fallback_name)
        if not any([location.get("nearestPlace"), location.get("island"), location.get("country")]):
            time.sleep(1)
            raw = reverse_lookup_raw(latitude, longitude, zoom=10)
            location = build_location(raw, latitude, longitude, fallback_name)
        return location
    except Exception as exc:
        return {
            "lookupStatus": "failed",
            "lookupProvider": LOOKUP_PROVIDER,
            "lookupError": str(exc),
            "displayName": fallback_name,
            "shortName": fallback_name,
        }
