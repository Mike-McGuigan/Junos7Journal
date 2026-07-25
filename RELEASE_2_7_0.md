# Release 2.7.0 - Voyage Playback and Map Usability

This release makes the voyage map easier to read as the route crosses earlier tracks, and improves the Captain's Dashboard workflow for adding new route points.

## Included changes

- Adds directional arrows at regular distance intervals along the rendered route geometry.
- Centres the directional route arrows so they sit cleanly on the plotted line.
- Limits map zoom levels to avoid unavailable high-zoom tiles and repeated world copies.
- Adds voyage playback controls with play/pause, progress scrubber, five speed levels and optional follow mode.
- Adds an extra-slow playback speed for more relaxed route review.
- Uses the same manual sea-waypoint geometry for route arrows and playback, so curves and crossings match the plotted track.
- Highlights the active route point as playback moves through the voyage.
- Moves the selected route-point detail cards beside the map on larger screens.
- Updates the Captain's Dashboard functional panels so only one panel is expanded at a time.
- Scrolls newly opened Captain's Dashboard panels into view so the section header remains visible.
- Defaults the Captain's Dashboard date field to the current date.
- Removes the old `East Coast Corfu` default from the new location name field.
- Adds placeholder text for empty location or passage names.
- Updates version/build metadata to `2.7.0`.

## Files changed

See `PATCH_MANIFEST_2_7_0.txt`.

## Build

After extracting this changed-files package over your current `main` branch, run:

```bash
python tools/build_site.py
```

The generated top-level `site/` directory is intentionally not included in this package.

## Validation checklist

- Confirm the site version displays as `2.7.0`.
- Confirm voyage route arrows appear at regular distance intervals.
- Confirm directional arrows sit centred on the route line.
- Confirm the map cannot zoom in far enough to show unavailable tile messages.
- Confirm the map cannot zoom out far enough to show repeated world copies.
- Confirm route arrows follow the curved/manual sea-waypoint geometry rather than only straight route-node segments.
- Confirm voyage playback can play, pause, scrub and change speed.
- Confirm the slowest playback speed is slower than the previous v2.7.0 build.
- Confirm the playback marker follows the rendered route.
- Confirm the highlighted route point updates during playback.
- Confirm selected route-point detail cards appear to the right of the map on desktop-width screens.
- Confirm the optional follow mode pans the map as playback moves.
- Confirm the Captain's Dashboard keeps only one functional panel open at a time.
- Confirm opening a Captain's Dashboard panel scrolls to the top of that panel.
- Confirm the new-position date defaults to today's date.
- Confirm the new-position location field starts empty and shows `Enter location or passage name`.
- Confirm existing voyage statistics remain aligned with the v2.6.3 passage calculation rules.

## Git workflow

Start from the released `main` branch:

```bash
git switch main
git pull --ff-only origin main
git switch -c release/v2.7.0
```

Extract the changed-files ZIP into the repository, then rebuild:

```bash
python tools/build_site.py
```

Review the changes:

```bash
git status
git diff --stat
git diff
```

Commit the release:

```bash
git add .
git commit -m "Release v2.7.0 voyage playback and map usability"
```

Merge back to `main`:

```bash
git switch main
git pull --ff-only origin main
git merge --no-ff release/v2.7.0 -m "Merge release v2.7.0"
```

Tag and push:

```bash
git tag -a v2.7.0 -m "Juno's 7 Journal v2.7.0"
git push origin main
git push origin v2.7.0
```

Clean up the release branch:

```bash
git branch -d release/v2.7.0
git push origin --delete release/v2.7.0
```

If the release branch was never pushed, the final remote-delete command may report that the branch does not exist. That is harmless.
