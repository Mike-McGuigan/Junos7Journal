# Juno's 7 Journal v2.1.0 — Geographic Intelligence

## What changed

- Adds reverse geocoding during manual location publishing.
- Stores friendly geographic metadata on new route points.
- Carries the friendly location into `dashboard.json`.
- Updates the Captain's Dashboard to show the enriched current location.
- Updates route map popups and timeline entries to display friendly place names when present.
- Backfills the existing v2.0.1 route with consistent `location` metadata.

## Install

Copy/extract this zip over the root of the repository and allow Windows to replace files.

Then run:

```bash
python tools/build_site.py
```

Then start the Captain's Dashboard and publish the yacht's new position.

## Notes

Reverse geocoding is performed only from the local publish step in `tools/apply_manual_location.py`, not by public visitors to the website.
