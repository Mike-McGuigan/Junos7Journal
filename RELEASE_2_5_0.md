# Juno's 7 Mediterranean Journal v2.5.0

## Connected Storytelling

This minor release connects the gallery, journal, discoveries and voyage statistics more closely while keeping the existing source/build workflow intact.

### 1. Gallery classification audit

- Reviews all 42 canonical media records.
- Renames the visible **Crew** filter to **Crew Life** while retaining the compatible `crew` data key.
- Adds Crew Life to the sun-deck maintenance and teak-repair records.
- Removes Crew Life from yacht, wildlife and weather-led records where no crew-centred activity is shown.
- Adds visible category badges to every gallery card.
- Documents the audit in `GALLERY_CLASSIFICATION_2_5_0.md`.

### 2. Journal and gallery cross-linking

- Stores related journal-entry metadata against every canonical media record.
- Adds a **Media from this chapter** label to journal media.
- Adds links from every gallery card back to its related journal chapter.
- Keeps all 42 media records linked to at least one chapter.

### 3. Contextual Discovery enhancements

- Adds category filters to the discovery archive.
- Shows a live result count while filtering.
- Adds direct links from discoveries to their related journal chapter and the voyage map.
- Retains the original evidence, proximity and source links.

### 4. Route and dashboard statistics

Adds generated statistics for:

- 40 voyage legs
- average passage distance
- longest passage and its endpoints
- countries visited and country names
- existing total distance and manual sea-route coverage

For the current route data, the build reports approximately **1,139.3 NM**, an average leg of **28.5 NM**, and a longest estimated leg of **223.9 NM**.

## Applying the changed-files ZIP

Extract the ZIP into the root of the local `Junos7Journal` repository and allow it to replace existing files.

The ZIP contains the updated source and generated `docs/` publishing tree, but deliberately excludes the generated `site/` build directory. Run the build command below before staging; it will recreate `site/` from the updated project files and include the resulting build output in the release commit according to the repository's normal workflow.

## Complete Git commands

```bash
git switch main
git pull --ff-only origin main
git switch -c release/v2.5.0

python tools/build_site.py

git status
git add --all
git commit -m "Release v2.5.0 connected storytelling"

git switch main
git merge --no-ff release/v2.5.0 -m "Merge release v2.5.0"
git tag -a v2.5.0 -m "Juno's 7 Journal v2.5.0"

git push origin main
git push origin v2.5.0

git branch -d release/v2.5.0
git status
```

The final `git status` should report that the working tree is clean.

## Pre-commit regression fixes

This replacement package also corrects issues found during initial testing before the release was committed:

- Removed the visible `#` permalink marker from every journal card.
- Kept **Media from this chapter** inside the media column so alternating journal layouts remain two-column.
- Corrected discovery filter and action-button contrast in their light-page context.
- Added post-render journal anchor scrolling for dynamically generated entries.
- Added stop-specific voyage deep links so discovery map links open and select the intended stop.

## Voyage summary visual polish

The final pre-commit package also updates **Voyage so far**:

- gives the Current Location card additional width on larger screens and safe text wrapping at every size;
- adds a consistent set of restrained outline icons to the summary cards;
- uses the exact approved filled Juno's 7 profile from the voyage-summary mock-up, supplied as a transparent PNG so the distinctive yacht remains recognisable at card size;
- keeps the icon treatment decorative and accessible by hiding it from assistive technology;
- collapses the widened location card back to a single column on smaller screens.
