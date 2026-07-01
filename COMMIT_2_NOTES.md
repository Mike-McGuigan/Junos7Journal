# Commit 2 - Geographic data normalisation

This commit keeps the UI unchanged and improves the publish-time geography layer.

## Changes

- Moves reverse-geocoding logic into `tools/geo_lookup.py`.
- Requests English language results from Nominatim.
- Normalises common Greek place names returned in local script.
- Adds conservative island inference for the current voyage area.
- Keeps the existing JSON schema:
  - `routePoint.location`
  - `tracker.location`
  - `tracker.latestFriendlyLocation`

## Test

1. Extract over repo root while on `feature/geographic-intelligence`.
2. Restart Captain's Dashboard.
3. Publish one test location.
4. Check `docs/data/dashboard.json` and `docs/data/route.json` for English-friendly `location.displayName`.

Commit message:

```bash
git add .
git commit -m "Normalise geographic lookup metadata"
git push
```
