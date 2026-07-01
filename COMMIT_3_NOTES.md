# Commit 3 - Geographic Intelligence Engine

This patch separates geographic lookup logic into `tools/geo_lookup.py` and makes the lookup output more suitable for an English-language voyage journal.

## Changes

- Adds `tools/geo_lookup.py`.
- Uses Nominatim with `Accept-Language: en`.
- Adds a small curated voyage gazetteer for known Greek island stops.
- Produces friendlier `location.displayName` values such as `Near Corfu Town, Corfu, Greece`.
- Keeps the existing JSON schema intact.
- Refines the dashboard current-location card so the manually entered name remains the title and the lookup becomes the subtitle.

## Test

1. Extract over repo root on `feature/geographic-intelligence`.
2. Restart Captain's Dashboard.
3. Publish a test location.
4. Check `docs/data/dashboard.json` and `docs/data/route.json` for `tracker.location.displayName` and `routePoint.location.displayName`.
5. Run `python tools/build_site.py`.
