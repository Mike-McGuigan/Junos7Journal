#!/usr/bin/env python3
"""Voyage routing helpers for Juno's 7 Journal.

This module enriches route.json with optional sea-aware route geometry.

The normal route points remain the source of truth for stops. Optional geometry
is stored separately in content/routes/voyage-geometry.json so we can add manual
sea waypoints for legs that would otherwise draw across land.
"""

from __future__ import annotations

from math import asin, cos, radians, sin, sqrt
from pathlib import Path
import json
from typing import Any

EARTH_RADIUS_KM = 6371.0088
KM_PER_NM = 1.852


def haversine_km(a: dict[str, Any] | list[float], b: dict[str, Any] | list[float]) -> float:
    """Return great-circle distance in kilometres between two points."""
    if isinstance(a, dict):
        lat1, lng1 = float(a["lat"]), float(a["lng"])
    else:
        lat1, lng1 = float(a[0]), float(a[1])

    if isinstance(b, dict):
        lat2, lng2 = float(b["lat"]), float(b["lng"])
    else:
        lat2, lng2 = float(b[0]), float(b[1])

    d_lat = radians(lat2 - lat1)
    d_lng = radians(lng2 - lng1)
    h = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lng / 2) ** 2
    return 2 * EARTH_RADIUS_KM * asin(sqrt(h))


def km_to_nm(km: float) -> float:
    return km / KM_PER_NM


def point_key(point: dict[str, Any]) -> str:
    """Stable-ish key for a route point without requiring historical IDs."""
    title = point.get("title") or point.get("name") or "route-stop"
    date = point.get("date") or "unknown-date"
    return f"{date}::{title}"


def leg_key(previous: dict[str, Any], current: dict[str, Any]) -> str:
    return f"{point_key(previous)} -> {point_key(current)}"


def normalise_geometry(previous: dict[str, Any], current: dict[str, Any], waypoints: list[Any] | None) -> list[list[float]]:
    """Return a full geometry from previous point to current point.

    The optional waypoints file should normally contain only intermediate points,
    but this function tolerates a full geometry as well.
    """
    start = [float(previous["lat"]), float(previous["lng"])]
    end = [float(current["lat"]), float(current["lng"])]

    raw = waypoints or []
    geometry: list[list[float]] = []
    for item in raw:
        if isinstance(item, dict):
            geometry.append([float(item["lat"]), float(item["lng"])])
        else:
            geometry.append([float(item[0]), float(item[1])])

    def same_point(a: list[float], b: list[float]) -> bool:
        return round(a[0], 6) == round(b[0], 6) and round(a[1], 6) == round(b[1], 6)

    if not geometry or not same_point(geometry[0], start):
        geometry.insert(0, start)
    if not same_point(geometry[-1], end):
        geometry.append(end)

    return geometry


def geometry_distance_nm(geometry: list[list[float]]) -> float:
    total_km = 0.0
    for i in range(1, len(geometry)):
        total_km += haversine_km(geometry[i - 1], geometry[i])
    return round(km_to_nm(total_km), 1)


def load_geometry(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"schemaVersion": 1, "legs": []}
    return json.loads(path.read_text(encoding="utf-8"))


def find_waypoints(geometry_data: dict[str, Any], previous: dict[str, Any], current: dict[str, Any], index: int) -> list[Any] | None:
    """Find optional manual sea waypoints for a leg.

    Supported matching styles:
    - fromIndex / toIndex, where toIndex is the current route point index.
    - key, using '<date>::<title> -> <date>::<title>'.
    - fromDate/fromTitle/toDate/toTitle for readable explicit matching.
    """
    key = leg_key(previous, current)
    prev_title = previous.get("title") or previous.get("name")
    cur_title = current.get("title") or current.get("name")

    for leg in geometry_data.get("legs", []):
        if leg.get("fromIndex") == index - 1 and leg.get("toIndex") == index:
            return leg.get("waypoints") or leg.get("geometry")
        if leg.get("key") == key:
            return leg.get("waypoints") or leg.get("geometry")
        if (
            leg.get("fromDate") == previous.get("date")
            and leg.get("toDate") == current.get("date")
            and leg.get("fromTitle") in {None, prev_title, previous.get("name")}
            and leg.get("toTitle") in {None, cur_title, current.get("name")}
        ):
            return leg.get("waypoints") or leg.get("geometry")
    return None


def enrich_route(route: list[dict[str, Any]], geometry_data: dict[str, Any]) -> dict[str, Any]:
    """Add leg distance and geometry metadata to each route point after the first."""
    total_direct = 0.0
    total_estimated = 0.0
    routed_legs = 0

    for i, point in enumerate(route):
        point.setdefault("title", point.get("name", "Route stop"))
        if i == 0:
            point.pop("legFromPrevious", None)
            continue

        previous = route[i - 1]
        direct_nm = round(km_to_nm(haversine_km(previous, point)), 1)
        waypoints = find_waypoints(geometry_data, previous, point, i)
        geometry = normalise_geometry(previous, point, waypoints)
        estimated_nm = geometry_distance_nm(geometry)
        has_manual_geometry = bool(waypoints)

        point["legFromPrevious"] = {
            "fromTitle": previous.get("title") or previous.get("name"),
            "toTitle": point.get("title") or point.get("name"),
            "distanceDirectNm": direct_nm,
            "distanceEstimatedNm": estimated_nm,
            "usesManualSeaRoute": has_manual_geometry,
            "geometry": geometry,
        }

        total_direct += direct_nm
        total_estimated += estimated_nm
        if has_manual_geometry:
            routed_legs += 1

    return {
        "routeStops": len(route),
        "distanceDirectNm": round(total_direct, 1),
        "distanceEstimatedNm": round(total_estimated, 1),
        "manualSeaRouteLegs": routed_legs,
    }


def enrich_route_file(route_path: Path, geometry_path: Path) -> dict[str, Any]:
    if not route_path.exists():
        return {}
    route = json.loads(route_path.read_text(encoding="utf-8"))
    geometry_data = load_geometry(geometry_path)
    stats = enrich_route(route, geometry_data)
    route_path.write_text(json.dumps(route, indent=2, ensure_ascii=False), encoding="utf-8")
    return stats
