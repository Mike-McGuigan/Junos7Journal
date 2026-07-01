#!/usr/bin/env python3
"""Geographic lookup helpers for Juno's 7 Journal.

The public site is static. These helpers are used only by the local publishing
workflow so that each route point is enriched once when it is published.
"""

from __future__ import annotations

from math import asin, cos, radians, sin, sqrt
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json

NOMINATIM_URL = "https://nominatim.openstreetmap.org/reverse"
USER_AGENT = "Junos7Journal/2.2-feature local-publishing-tool"
LOOKUP_PROVIDER = "OpenStreetMap Nominatim"

# Small curated nautical gazetteer for the areas Juno's 7 is currently visiting.
# This is deliberately simple and dependency-free. Nominatim provides the broad
# administrative data; this list makes the result read like a voyage journal.
KNOWN_PLACES = [
    # Ionian islands
    {"name": "Corfu Town", "island": "Corfu", "country": "Greece", "lat": 39.6243, "lng": 19.9217},
    {"name": "Kassiopi", "island": "Corfu", "country": "Greece", "lat": 39.7889, "lng": 19.9217},
    {"name": "Gouvia", "island": "Corfu", "country": "Greece", "lat": 39.6526, "lng": 19.8476},
    {"name": "Benitses", "island": "Corfu", "country": "Greece", "lat": 39.5431, "lng": 19.9159},
    {"name": "Gaios", "island": "Paxos", "country": "Greece", "lat": 39.1973, "lng": 20.1859},
    {"name": "Sami", "island": "Kefalonia", "country": "Greece", "lat": 38.2537, "lng": 20.6464},
    {"name": "Vathy", "island": "Ithaca", "country": "Greece", "lat": 38.3654, "lng": 20.7183},
    {"name": "Frikes", "island": "Ithaca", "country": "Greece", "lat": 38.4595, "lng": 20.6652},
    {"name": "Zakynthos Town", "island": "Zakynthos", "country": "Greece", "lat": 37.7882, "lng": 20.8990},
    # Aegean / Dodecanese / Cyclades
    {"name": "Lindos", "island": "Rhodes", "country": "Greece", "lat": 36.0917, "lng": 28.0856},
    {"name": "Emporio / Chalki Harbour", "island": "Chalki", "country": "Greece", "lat": 36.2220, "lng": 27.6110},
    {"name": "Symi Harbour / Gialos", "island": "Symi", "country": "Greece", "lat": 36.6170, "lng": 27.8380},
    {"name": "Mandraki", "island": "Nisyros", "country": "Greece", "lat": 36.6110, "lng": 27.1330},
    {"name": "Kos Town", "island": "Kos", "country": "Greece", "lat": 36.8930, "lng": 27.2890},
    {"name": "Lipsi Harbour", "island": "Lipsi", "country": "Greece", "lat": 37.2950, "lng": 26.7660},
    {"name": "Skala", "island": "Patmos", "country": "Greece", "lat": 37.3240, "lng": 26.5450},
    {"name": "Katapola", "island": "Amorgos", "country": "Greece", "lat": 36.8270, "lng": 25.8630},
    {"name": "Ios Port / Ormos", "island": "Ios", "country": "Greece", "lat": 36.7220, "lng": 25.2720},
]

REGION_EN = {
    "Περιφέρεια Ιονίων Νήσων": "Ionian Islands",
    "Περιφέρεια Νοτίου Αιγαίου": "South Aegean",
    "Ιόνια Νησιά": "Ionian Islands",
    "Νότιο Αιγαίο": "South Aegean",
}

COUNTRY_EN = {
    "Ελλάς": "Greece",
    "Ελλάδα": "Greece",
    "Hellas": "Greece",
}


def _nice_join(parts: list[str | None], sep: str = ", ") -> str:
    out = []
    for part in parts:
        if part and part not in out:
            out.append(part)
    return sep.join(out)


def _haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    radius_km = 6371.0088
    d_lat = radians(lat2 - lat1)
    d_lng = radians(lng2 - lng1)
    a = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lng / 2) ** 2
    return 2 * radius_km * asin(sqrt(a))


def _nearest_known_place(lat: float, lng: float) -> dict | None:
    best = None
    for place in KNOWN_PLACES:
        km = _haversine_km(lat, lng, place["lat"], place["lng"])
        candidate = {**place, "distanceKm": round(km, 1), "distanceNm": round(km / 1.852, 1)}
        if best is None or km < best["distanceKm"]:
            best = candidate
    # Keep this deliberately generous for island/coastal positions where the
    # yacht may be several miles offshore.
    if best and best["distanceKm"] <= 35:
        return best
    return None


def _normalise_country(value: str | None) -> str | None:
    if not value:
        return None
    return COUNTRY_EN.get(value, value)


def _normalise_region(value: str | None) -> str | None:
    if not value:
        return None
    return REGION_EN.get(value, value)


def _call_nominatim(lat: float, lng: float) -> dict:
    params = urlencode(
        {
            "format": "jsonv2",
            "lat": f"{lat:.6f}",
            "lon": f"{lng:.6f}",
            "zoom": 10,
            "addressdetails": 1,
            "namedetails": 1,
        }
    )
    req = Request(
        f"{NOMINATIM_URL}?{params}",
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "Accept-Language": "en",
        },
    )
    with urlopen(req, timeout=12) as response:
        return json.loads(response.read().decode("utf-8"))


def reverse_lookup(lat, lng, fallback_name: str = "Manual location") -> dict:
    """Return travel-friendly geographic metadata for a lat/lng."""
    lat_f = float(lat)
    lng_f = float(lng)

    try:
        raw = _call_nominatim(lat_f, lng_f)
    except Exception as exc:
        nearest = _nearest_known_place(lat_f, lng_f)
        if nearest:
            display = _nice_join([f"Near {nearest['name']}", nearest["island"], nearest["country"]])
            return {
                "lookupStatus": "partial",
                "lookupProvider": LOOKUP_PROVIDER,
                "lookupError": str(exc),
                "displayName": display,
                "shortName": _nice_join([nearest["name"], nearest["island"]]),
                "country": nearest["country"],
                "countryCode": "GR" if nearest["country"] == "Greece" else None,
                "island": nearest["island"],
                "nearestPlace": nearest["name"],
                "nearestPlaceDistanceKm": nearest["distanceKm"],
                "nearestPlaceDistanceNm": nearest["distanceNm"],
                "lookupSource": "curated fallback gazetteer",
            }
        return {
            "lookupStatus": "failed",
            "lookupProvider": LOOKUP_PROVIDER,
            "lookupError": str(exc),
            "displayName": fallback_name,
            "shortName": fallback_name,
        }

    address = raw.get("address", {}) or {}
    country = _normalise_country(address.get("country"))
    country_code = (address.get("country_code") or "").upper() or None
    region = _normalise_region(address.get("state") or address.get("region"))
    county = address.get("county")
    municipality = address.get("municipality") or address.get("city") or address.get("town")
    island = address.get("island")
    nearest_osm = (
        address.get("city")
        or address.get("town")
        or address.get("village")
        or address.get("hamlet")
        or address.get("municipality")
        or address.get("county")
    )
    local_area = address.get("suburb") or address.get("neighbourhood") or address.get("quarter")

    known = _nearest_known_place(lat_f, lng_f)
    nearest_place = nearest_osm
    if known:
        nearest_place = known["name"]
        island = island or known["island"]
        country = country or known["country"]
        if known["country"] == "Greece":
            country_code = country_code or "GR"

    if known:
        display = _nice_join([f"Near {known['name']}", known["island"], known["country"]])
        short_name = _nice_join([known["name"], known["island"]])
    elif island and nearest_place and island != nearest_place:
        display = _nice_join([f"Near {nearest_place}", island, country])
        short_name = _nice_join([nearest_place, island])
    elif nearest_place:
        display = _nice_join([f"Near {nearest_place}", region, country])
        short_name = _nice_join([nearest_place, municipality or county])
    elif island:
        display = _nice_join([island, country])
        short_name = island
    else:
        display = fallback_name
        short_name = fallback_name

    result = {
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

    if known:
        result.update(
            {
                "nearestKnownPlace": known["name"],
                "nearestKnownPlaceDistanceKm": known["distanceKm"],
                "nearestKnownPlaceDistanceNm": known["distanceNm"],
                "lookupSource": "OpenStreetMap Nominatim + curated voyage gazetteer",
            }
        )
    else:
        result["lookupSource"] = "OpenStreetMap Nominatim"

    return result
