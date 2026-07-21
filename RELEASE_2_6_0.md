# Release 2.6.0 — Navigation & Discovery

## Scope

This release introduces grouped voyage-wide search and bidirectional links between journal entries and voyage-map stops. It also adds two factual Zadar entries from 20 July.

## Changed source files

See `PATCH_MANIFEST_2_6_0.txt`. The release archive deliberately excludes `site/`; rebuild it locally from `docs/`.

## Branch

```bash
git switch main
git pull
git switch -c release/v2.6.0
```

## Apply and build

Extract the changed-files ZIP over the repository root, then run:

```bash
python tools/build_site.py
```

## Testing

```bash
python -m json.tool docs/data/journal.json > /dev/null
python -m json.tool docs/data/route.json > /dev/null
python -m json.tool docs/data/media.json > /dev/null
```

Manual checks:

1. Search for `dolphin`, `Zadar`, `scampi`, `Reposado` and `storm`; confirm grouped results and result counts.
2. Open a journal **View on map** link; confirm the named map tab is reused, the correct stop is centred and its popup opens.
3. From a related map stop, open **Read journal entry** and confirm the correct chapter is shown.
4. Check oldest/newest journal ordering, gallery filters, lightbox and mobile layout.
5. Confirm the Antiquus and Toni entries are text-only and contain no VesselFinder accident-scene screenshot.

## Commit

```bash
git add VERSION ROADMAP.md RELEASE_2_6_0.md PATCH_MANIFEST_2_6_0.txt CHANGELOG.md tools/build_site.py docs/index.html docs/assets/css/style.css docs/assets/js/app.js docs/assets/js/dashboard.js docs/data/journal.json content/journal/2026/2026-07-20-antiquus-zadar.md content/journal/2026/2026-07-20-toni-accident.md
git commit -m "Release v2.6.0 navigation and discovery"
```

## Merge, tag and push

```bash
git switch main
git merge --no-ff release/v2.6.0
git tag -a v2.6.0 -m "Juno's 7 Journal v2.6.0"
git push origin main
git push origin v2.6.0
```

## Cleanup

```bash
git branch -d release/v2.6.0
git push origin --delete release/v2.6.0
```

## Rollback

Before merge:

```bash
git switch main
git branch -D release/v2.6.0
```

After merge but before publishing further work:

```bash
git revert -m 1 <merge-commit-sha>
git push origin main
```

- Included the original sushi-boat photograph and linked it to the journal entry and gallery.

## Corrected reissue

This reissue removes the VesselFinder/AIS screenshot from the Zadar Reposado journal entry, in line with the agreed editorial decision not to include tracking screenshots in the journal. The Antiquus Sushi & More meal photograph remains included.

After extracting the patch, delete:

```text
docs/media/photos/2026-07-19-zadar-reposado-ais.png
```

Then rebuild `site/` with `python tools/build_site.py`.
