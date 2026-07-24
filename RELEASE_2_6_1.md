# Release 2.6.1 - Maintenance & Editorial Consistency

## Scope

This maintenance release fixes the recurring version rollback to `2.2.0`, clarifies country statistics as **Countries visited**, removes Albania from the visited-country count because it is only present on an underway transit marker, and removes the stale VesselFinder/AIS media file from the source media folder.

This re-issued package also includes the recovered media supplied after the initial v2.6.1 package: the Kablin Bay aft-deck photograph, Sakarun beach setup photograph, Michelle snorkelling accident photograph, dolphin **Music Edit**, cave excursion and two onboard CCTV Crew Life clips.

## Release decisions

- Root `VERSION` is the authoritative version source.
- Manual-location publishing tools must preserve root `VERSION` and must not hard-code historical release versions.
- `journal.json` keeps its legacy embedded route copy aligned with `docs/data/route.json` during builds.
- Country statistics count visited stops/anchorages/moorings, not underway transit points.
- Albania remains in the route as an underway marker but is not counted as visited.
- Undated recovered clips are preserved as Crew Life / season-highlight entries rather than forced into the dated voyage chronology.
- The dolphin **Music Edit** is attached to the existing bow-dolphin encounter and is not counted as a separate dolphin sighting.
- Onboard CCTV clips are labelled by source as **Onboard CCTV**, not by the person who later shared them.

## Build

```bash
python tools/build_site.py
```

## Validation

```bash
python -m json.tool docs/data/journal.json > /dev/null
python -m json.tool docs/data/route.json > /dev/null
python -m json.tool docs/data/media.json > /dev/null
python -m py_compile tools/build_site.py tools/voyage_routing.py tools/apply_manual_location.py tools/admin_publish_server.py
```

Manual checks:

1. Confirm the version displays as `2.6.1` after rebuilding.
2. Confirm the home and dashboard cards say **Countries visited**.
3. Confirm the country count is `2` with `Greece · Croatia`.
4. Confirm Albania still appears only as an underway transit marker in the route data.
5. Confirm the VesselFinder/AIS screenshot is not shown in the journal or gallery.
6. Confirm the new Kablin Bay, Michelle, Sakarun Beach and Zadar Anchorage entries appear in the journal in the expected order.
7. Confirm the cave excursion and onboard CCTV clips appear as undated Crew Life highlights.
8. Confirm the dolphin **Music Edit** appears under the existing 13 July dolphin entry.
9. Confirm search, gallery filters, journal links and voyage map links still work.

## Files to delete

Changed-files ZIP extraction cannot delete existing files. After extracting this release, delete:

```bash
rm docs/media/photos/2026-07-19-zadar-reposado-ais.png
rm docs/data/dashboard.json.bak-1-0-5
rm docs/data/dashboard.json.bak-1-2-0
rm docs/data/dashboard.json.bak-geo-1
rm docs/data/dashboard.json.bak-geo-2
rm docs/data/route.json.bak-geo-1
rm docs/data/route.json.bak-geo-2
rm docs/data/version.json.bak-geo-1
rm docs/data/version.json.bak-geo-2
rm content/routes/route-so-far.json.bak-geo-1
rm content/routes/route-so-far.json.bak-geo-2
```

## Git workflow

### Create release branch

```bash
git switch main
git pull
git switch -c release/v2.6.1
```

### Apply release package

Extract the changed-files ZIP over the repository root, then delete the stale AIS file and stale backup files listed above.

### Build and test

```bash
python tools/build_site.py
python -m json.tool docs/data/journal.json > /dev/null
python -m json.tool docs/data/route.json > /dev/null
python -m json.tool docs/data/media.json > /dev/null
python -m py_compile tools/build_site.py tools/voyage_routing.py tools/apply_manual_location.py tools/admin_publish_server.py
```

### Review

```bash
git status
git diff --stat
git diff
```

### Commit

```bash
git add .
git commit -m "Release v2.6.1 maintenance and editorial consistency"
```

### Merge

```bash
git switch main
git merge --no-ff release/v2.6.1 -m "Merge release v2.6.1"
```

### Tag

```bash
git tag -a v2.6.1 -m "Juno's 7 Journal v2.6.1"
```

### Push

```bash
git push origin main
git push origin v2.6.1
```

### Delete release branch

```bash
git branch -d release/v2.6.1
git push origin --delete release/v2.6.1
```

## Rollback

Before merge:

```bash
git switch main
git branch -D release/v2.6.1
```

After merge:

```bash
git revert -m 1 <merge-commit-sha>
git push origin main
```
