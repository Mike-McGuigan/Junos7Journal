# Manual Waypoint Editor

Adds a Captain's Dashboard route editor for optional sea-aware waypoints between existing stops.

## Workflow

1. Start Captain's Dashboard.
2. Select a voyage leg.
3. Click Edit Leg.
4. Click intermediate sea waypoints on the map.
5. Save Route.
6. The local server writes `content/routes/voyage-geometry.json` and runs `tools/build_site.py`.

This does not auto-commit. Review the generated route and commit/push when happy.
