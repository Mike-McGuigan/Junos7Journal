# Juno's 7 Journal v2.7.4

## Release summary

v2.7.4 adds safety guards around the Captain's Dashboard so `localhost:8765` cannot silently point at an old extracted repository copy.

## Included changes

- Shows the active dashboard version, release title, branch, working-tree state and serving repository root in the dashboard health panel.
- Refuses to start the dashboard if port `8765` is already being served by a different repository folder.
- Warns clearly if port `8765` is occupied by another non-dashboard process.
- Removes duplicate repository output from the dashboard starter.
- Removes the non-actionable credential-helper warning from the visible dashboard health checklist.
- Includes the repository path in local save confirmations for route updates, stop edits and manual sea-route geometry.
- Improves manual-location filename sanitising so passage names such as `Crotone -> Valletta` become clean `crotone-to-valletta` filenames.
- Prevents stale local dashboard JavaScript from being reused after rebuilds by adding no-cache headers and a versioned admin script reference.
- Fixes the manual sea-waypoint editor so the base route is removed during leg editing, leaving a single cyan editable route and avoiding the appearance of a duplicate leg.
- Fixes manual sea-waypoint ordering so each click is appended as the next waypoint instead of being reordered around the nearest route segment.
- Updates version and build metadata to `2.7.4`.

## Validation performed

- Ran the site build successfully from the live local repository.
- Ran JavaScript syntax validation for the Captain's Dashboard script.
- Queried the local dashboard health endpoint and confirmed it reports the live repository root.
- Browser-tested the Crotone to Valletta leg editor: Edit Leg shows only the cyan editable leg, the first waypoint click adds one waypoint to that leg, and Cancel restores the normal route.
- Browser-tested ten waypoint clicks: markers stayed numbered `1` through `10` in click order, with no route save performed.

## Apply and release commands

These commands are only needed if applying from a changed-files package. If Codex has already updated the live repository directly, review the working tree and commit the files in place.

```bash
git status
git add .
python tools/build_site.py
git status
git diff --cached

git commit -m "Release v2.7.4 dashboard safety guards"
git tag -a v2.7.4 -m "Juno's 7 Journal v2.7.4"
git push origin main
git push origin v2.7.4
```
