# Project Notes — Juno's 7 Mediterranean Journal

Current version: 2.7.1
Release: Maintenance & Editorial Consistency

## Operating model

- `docs/` is the source web site and GitHub Pages tree.
- `site/` is rebuilt from `docs/` by `tools/build_site.py` as a clean local/export copy.
- The canonical journal source is `docs/data/journal.json`: a JSON object containing `schemaVersion`, an `entries` list, and the embedded `media` and `route` lists. `docs/data/media.json` and `docs/data/route.json` are the canonical supporting indexes.
- `site/` is generated output, not an input source. Do not edit it as the authoritative copy or use its files to replace `docs/` during normal work.
- The Captain's Dashboard runs locally and uses existing Git credentials.
- Public free AIS may be stale; manual map-click updates are labelled by position-source precision.
- Exactly one route point should have `"phase": "current"`.

## Daily publishing workflow

1. Double-click `Start Captains Dashboard.bat`.
2. Click the map.
3. Enter the location name.
4. Click Save Route Update.
5. Review the local build, then commit and push when ready.

## Safe build process

1. Work from the repository root: `C:\@GitRepos\Junos7Journal`.
2. Edit the canonical files under `docs/` and `docs/data/`; keep journal entries inside the `entries` list in `docs/data/journal.json`.
3. Run `python tools/build_site.py` only after the source JSON has been checked. The build validates the journal structure before it updates embedded media, route data, dashboard statistics or generated metadata.
4. Review the build output and the generated files under `site/`. Treat `site/` as disposable output that must match `docs/` after a successful build.
5. If the build reports a journal-structure error, stop and repair `docs/data/journal.json`; do not continue by copying legacy aggregate data into the source.

## Eat and Drink content rules

- Add flavour content to the relevant journal entry's `flavourOf` block in `docs/data/journal.json`; the Eat page renders these cards from the JSON.
- Every `flavourOf` card must include a project-local image under `docs/assets/images/flavour/`. Generate a matching image when suitable source media is not available.
- Keep region-specific products under their specific island label. Use `Balearic Islands` only for genuinely shared or fallback styles.
- Drink cards should not link back to individual journal chapters. Keep the page-level Return to the journal link, and add supermarket or retailer product links where a useful current product or category exists.
- Rebuild with `tools/build_site.py` after changing `docs/`, then verify the corresponding `site/` output contains the same content and assets.
