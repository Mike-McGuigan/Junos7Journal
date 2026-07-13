# Project Notes — Juno's 7 Mediterranean Journal

Current version: 2.2.0
Release: Journal Experience

## Operating model

- `docs/` is the source web site and GitHub Pages tree.
- `site/` is rebuilt from `docs/` by `tools/build_site.py` as a clean local/export copy.
- The Captain's Dashboard runs locally and uses existing Git credentials.
- Public free AIS may be stale; manual map-click updates are labelled by precision.
- Exactly one route point should have `"phase": "current"`.

## Daily publishing workflow

1. Double-click `Start Captains Dashboard.bat`.
2. Click the map.
3. Enter the location name.
4. Click Publish.
5. Check GitHub Actions.
