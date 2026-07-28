# Juno's 7 Journal v2.7.3

## Release summary

v2.7.3 is a focused Captain's Dashboard maintenance release that restores reliable manual sea-route leg editing after duplicate same-position route points were added.

## Included changes

- Prevents zero-distance duplicate route-point legs from opening in the Voyage Route Editor.
- Labels zero-distance entries in the leg selector as `same position`.
- Defaults the leg selector to the latest non-zero leg.
- Keeps the selected editable leg highlighted with the blue dashed line.
- Inserts newly clicked manual sea waypoints into the nearest part of the active leg instead of appending them after the final waypoint.
- Updates version, build metadata, changelog and roadmap to `2.7.3`.

## Validation performed

- Ran the site build successfully.
- Ran JavaScript syntax validation for the updated dashboard route editor.
- Confirmed the changed-files package excludes the generated `site/` directory.

## Apply and release commands

Run these from the repository root after extracting the changed-files ZIP.

```bash
git status
git switch main
git pull --ff-only origin main
git switch -c release/v2.7.3

git add .
python tools/build_site.py
git status
git diff --cached

git commit -m "Release v2.7.3 route editor leg fix"

git switch main
git pull --ff-only origin main
git merge --no-ff release/v2.7.3 -m "Merge release v2.7.3"
git tag -a v2.7.3 -m "Juno's 7 Journal v2.7.3"

git push origin main
git push origin v2.7.3

git branch -d release/v2.7.3
```

If the release branch was pushed remotely, also run:

```bash
git push origin --delete release/v2.7.3
```
