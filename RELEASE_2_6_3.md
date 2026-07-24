# Release 2.6.3 - Passage Statistics Refinement

This small patch fixes the route statistics so the dashboard treats a passage as the continuous run between real stops and anchorages, rather than treating every underway/AIS route marker as a separate passage.

## Included changes

- Keeps all route nodes visible on the map.
- Keeps each node's `legFromPrevious` distance for popup and route-editor use.
- Adds collapsed passage statistics for dashboard summaries.
- Merges underway, AIS, milestone and explicit en-route markers into the surrounding passage for longest/average passage calculations.
- Updates average passage wording to say **passages** rather than **route legs**.
- Renames the homepage metric from **Longest leg** to **Longest passage**.
- Renames **Route stops** to **Route points** so underway markers are not implied to be physical stops.
- Updates version/build metadata to `2.6.3`.

## Files changed

See `PATCH_MANIFEST_2_6_3.txt`.

## Build

After extracting this changed-files package over your current `main` branch, run:

```bash
python tools/build_site.py
```

The generated top-level `site/` directory is intentionally not included in this package.

## Validation checklist

- Confirm the site version displays as `2.6.3`.
- Confirm the dashboard still shows every route node on the map.
- Confirm **Longest passage** is calculated across continuous passages rather than individual underway markers.
- Confirm **Average passage** says `across X passages`.
- Confirm **Route points** is shown instead of **Route stops**.
- Confirm route popups still show distance from the previous route node.
- Confirm **Countries visited** remains Greece and Croatia only unless Italy has been added as an actual stop.

## Git workflow

Start from the released `main` branch:

```bash
git switch main
git pull --ff-only origin main
git switch -c release/v2.6.3
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
git commit -m "Release v2.6.3 passage statistics refinement"
```

Merge back to `main`:

```bash
git switch main
git pull --ff-only origin main
git merge --no-ff release/v2.6.3 -m "Merge release v2.6.3"
```

Tag and push:

```bash
git tag -a v2.6.3 -m "Juno's 7 Journal v2.6.3"
git push origin main
git push origin v2.6.3
```

Clean up the release branch:

```bash
git branch -d release/v2.6.3
git push origin --delete release/v2.6.3
```

If the release branch was never pushed, the final remote-delete command may report that the branch does not exist. That is harmless.
