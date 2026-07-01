# Release 2.0.1 — Restore Historical Route

## Fix

v2.0.0 accidentally included a shortened placeholder route, which removed much of the historical voyage from the map.

This patch restores the full route history and keeps the latest current point behaviour.

## Apply

```bash
python tools/restore_historical_route.py
python tools/build_site.py
git add .
git commit -m "Restore historical voyage route"
git push
```
