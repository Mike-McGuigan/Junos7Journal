# Release 2.6.2 - Cave Location Refinement

This small patch refines the recovered cave excursion after the 13 July Vis-to-Komiža route review showed Juno's 7 making a clear loop down towards Biševo.

The cave clip is now labelled as **Likely Blue Cave, Biševo, Croatia**, but remains an undated season highlight because Cameron and Sophie have not directly confirmed the exact cave or date.

## Included changes

- Updates the cave journal entry from a generic Croatian Adriatic location to **Likely Blue Cave, Biševo, Croatia**.
- Keeps the wording cautious and evidence-based.
- Adds the 13 July Biševo route loop as supporting context without creating a false yacht stop.
- Updates the cave media title, caption and journal relationship.
- Updates version/build metadata to `2.6.2`.
- Updates `CHANGELOG.md`, `ROADMAP.md` and `PROJECT_NOTES.md`.

## Files changed

See `PATCH_MANIFEST_2_6_2.txt`.

## Build

After extracting this changed-files package over your current `main` branch, run:

```bash
python tools/build_site.py
```

The generated top-level `site/` directory is intentionally not included in this package.

## Validation checklist

- Confirm the site version displays as `2.6.2`.
- Confirm the cave entry appears as **Likely Blue Cave Excursion**.
- Confirm the cave location displays as **Likely Blue Cave, Biševo, Croatia**.
- Confirm the entry remains undated / Summer 2026 rather than being inserted into the 13 July chronology.
- Confirm the cave media caption mentions the likely Blue Cave/Biševo location.
- Confirm no new route stop has been created for the cave excursion.

## Git workflow

Start from the released `main` branch:

```bash
git switch main
git pull --ff-only origin main
git switch -c release/v2.6.2
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
git commit -m "Release v2.6.2 cave location refinement"
```

Merge back to `main`:

```bash
git switch main
git pull --ff-only origin main
git merge --no-ff release/v2.6.2 -m "Merge release v2.6.2"
```

Tag and push:

```bash
git tag -a v2.6.2 -m "Juno's 7 Journal v2.6.2"
git push origin main
git push origin v2.6.2
```

Clean up the release branch:

```bash
git branch -d release/v2.6.2
git push origin --delete release/v2.6.2
```

If the release branch was never pushed, the final remote-delete command may report that the branch does not exist. That is harmless.
