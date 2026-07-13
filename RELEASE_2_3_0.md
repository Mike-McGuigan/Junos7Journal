# Juno's 7 Journal v2.3.0 — Contextual Discovery

## What changed

- Added a curated Contextual Discovery data layer tied to actual voyage stops.
- Added eight source-backed discoveries across Kos, Cavtat, Polače, Korčula, the Pakleni Islands, Split, Vis and Komiža.
- Added the public **What They Almost Missed** discovery page.
- Added discovery cards inside matching journal chapters.
- Added discovery indicators, popups and selected-stop stories to the voyage map.
- Added a documented distance policy: close by default, exceptional only with evidence.
- Added `tools/contextual_discovery.py` to validate route matching, journal matching, proximity rules and source links.
- Added discovery counts to the journal and voyage dashboards.

## Apply as a changed-files patch

Create a release branch from the current v2.2.2 `main` branch:

```bash
git switch main
git pull --ff-only
git switch -c release/v2.3.0
```

Extract the patch over the repository root, allowing folders to merge and files to be replaced.

Build and preview:

```bash
python tools/contextual_discovery.py --check
python tools/build_site.py
python -m http.server 8000 --directory docs
```

Open `http://localhost:8000`, then review the journal, Discoveries page and voyage map.

Commit:

```bash
git add .
git commit -m "Release v2.3.0 Contextual Discovery"
git push -u origin release/v2.3.0
```

After approval, merge and tag in the normal way.
