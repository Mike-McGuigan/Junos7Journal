# Release 2.7.2 - Flavour Card Food Images

## Summary

This maintenance release adds optional images to the journal's **Flavour of the place** cards.

The images are deliberately treated as supporting editorial assets, not as yacht media:

- generated regional food images are labelled as illustrative;
- real journal meal photos are reused where available;
- no generated food image is added to the gallery media catalogue.

## Included changes

- Added optional image rendering for rich journal cards.
- Added card styling for food images and captions.
- Added three illustrative food assets:
  - `docs/assets/images/flavour/greek-island-table.png`
  - `docs/assets/images/flavour/dalmatian-seafood-table.png`
  - `docs/assets/images/flavour/calabrian-table.png`
- Added image metadata to all current **Flavour of the place** entries.
- Reused the existing Zut scampi and Zadar sushi meal photos for those flavour cards.
- Updated version metadata to `2.7.2`.

## Validation performed

- Ran `python tools/build_site.py`.
- Confirmed generated site reports version `2.7.2`.
- Confirmed all ten flavour cards have valid image references.
- Ran JavaScript syntax validation for `docs/assets/js/app.js`.
- Confirmed the changed-files ZIP excludes the generated `site/` directory.

## Git workflow

Run these commands from the repository root.

```bash
git switch main
git pull --ff-only origin main
git switch -c release/v2.7.2
```

Apply the changed files from this package, then rebuild:

```bash
python tools/build_site.py
```

Review and commit:

```bash
git status
git add .
git commit -m "Release v2.7.2 flavour card food images"
```

Merge to `main`:

```bash
git switch main
git pull --ff-only origin main
git merge --no-ff release/v2.7.2 -m "Merge release v2.7.2"
```

Tag and push:

```bash
git tag -a v2.7.2 -m "Juno's 7 Journal v2.7.2"
git push origin main
git push origin v2.7.2
```

Clean up the local release branch:

```bash
git branch -d release/v2.7.2
```

