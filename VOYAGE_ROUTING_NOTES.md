# Voyage Routing

This patch adds the foundation for sea-aware voyage routing.

## What changed

- Adds `tools/voyage_routing.py`.
- Adds `content/routes/voyage-geometry.json` for optional manual sea waypoints.
- Updates `tools/build_site.py` to enrich `docs/data/route.json` with:
  - `legFromPrevious.distanceDirectNm`
  - `legFromPrevious.distanceEstimatedNm`
  - `legFromPrevious.geometry`
  - `legFromPrevious.usesManualSeaRoute`
- Updates dashboard stats with:
  - `distanceDirectNm`
  - `distanceEstimatedNm`
  - `manualSeaRouteLegs`
- Updates map drawing to use the sea-aware geometry where available.

## How to add a sea-aware route

Add a leg to `content/routes/voyage-geometry.json`, for example:

```json
{
  "fromIndex": 16,
  "toIndex": 17,
  "description": "Paxos to Corfu via open water",
  "waypoints": [
    [39.33, 20.10],
    [39.48, 19.98],
    [39.58, 19.90]
  ]
}
```

The build will automatically include the previous and current stop coordinates, so `waypoints` should normally contain only intermediate sea points.
