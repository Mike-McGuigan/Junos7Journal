# Release 2.7.1 - Crotone Arrival and Dashboard Save Flow

This release records Juno's 7's first confirmed Italian stop and corrects the Captain's Dashboard wording so local saves are no longer described as public publishing.

## Included changes

- Adds **26 Jul - Arrival in Crotone** to the journal.
- Adds **Crotone Old Harbour, Calabria, Italy** as the associated journal/map location.
- Adds a Crotone contextual discovery covering ancient Kroton, Pythagoras and Capo Colonna.
- Adds **Flavour of Calabria** to the Crotone entry.
- Confirms **Italy** is included in **Countries visited** now that there is an actual Italian stop.
- Renames the Captain's Dashboard **Publish** action to **Save Route Update**.
- Makes the local dashboard save/build flow explicit: review locally, then commit and push to publish.
- Removes automatic commit/push behaviour from the dashboard route-update endpoint.
- Refreshes the dashboard after successful local route-update saves.
- Updates version/build metadata to `2.7.1`.

## Files changed

See `PATCH_MANIFEST_2_7_1.txt`.

## Build

After extracting this changed-files package over your current `main` branch, run:

```bash
python tools/build_site.py
```

The generated top-level `site/` directory is intentionally not included in this package.

## Validation checklist

- Confirm the site version displays as `2.7.1`.
- Confirm the journal includes **Arrival in Crotone**.
- Confirm the Crotone entry links to **Crotone Old Harbour, Calabria, Italy** on the map.
- Confirm the Crotone entry includes **Did you know?** and **Flavour of Calabria** cards.
- Confirm the Discoveries page includes the Crotone contextual discovery.
- Confirm **Countries visited** includes Greece, Croatia and Italy.
- Confirm the Captain's Dashboard button says **Save Route Update**, not **Publish**.
- Confirm saving a route update says it was saved locally.
- Confirm saving a route update refreshes the dashboard tab.
- Confirm saving from the dashboard does not commit or push automatically.

## Git workflow

Start from the released `main` branch:

```bash
git switch main
git pull --ff-only origin main
git switch -c release/v2.7.1
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
git commit -m "Release v2.7.1 Crotone arrival and dashboard save flow"
```

Merge back to `main`:

```bash
git switch main
git pull --ff-only origin main
git merge --no-ff release/v2.7.1 -m "Merge release v2.7.1"
```

Tag and push:

```bash
git tag -a v2.7.1 -m "Juno's 7 Journal v2.7.1"
git push origin main
git push origin v2.7.1
```

Clean up the release branch:

```bash
git branch -d release/v2.7.1
git push origin --delete release/v2.7.1
```

If the release branch was never pushed, the final remote-delete command may report that the branch does not exist. That is harmless.
