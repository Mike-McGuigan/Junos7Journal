# Juno’s 7 Journal Roadmap

This is the shared source of truth for release scope, deferred work and validation. Items must not quietly disappear: incomplete work is moved to **Deferred** or **Blocked** with a brief explanation.

## Current release

**v2.6.2 — Cave Location Refinement**

## Next release

Scope to be assigned after v2.6.2 is committed and tested.

## Current release scope

### Editorial refinement
- [x] Update the recovered cave excursion to **Likely Blue Cave, Biševo, Croatia**.
- [x] Keep the entry undated because the exact date and cave have not been directly confirmed by Cameron and Sophie.
- [x] Reference the 13 July Vis-to-Komiža route loop towards Biševo as supporting context without creating a false yacht stop.

## Backlog

### Journal and editorial
- [ ] Continue adding concise place-based entries for genuine stops and anchorages.
- [ ] Review new route labels for accurate harbour, bay, cove and island terminology.
- [ ] Preserve correct Croatian spelling and diacritics.
- [ ] Keep routine underway positions map-only unless something noteworthy happened.

### Notable encounters
- [ ] Add future encountered yachts with builder, length and a concise interesting fact.
- [ ] Include a current published charter guide where available; otherwise state that no public charter is offered.
- [ ] Consider occasional “Harbour line-up” cards when several notable vessels share a harbour.

### Navigation and discovery
- [ ] Refine search ranking as the archive grows.
- [ ] Consider optional content filters only if search results become difficult to scan.
- [ ] Explore memory highlights and “On this day” after the core journal is mature.

### Editorial workflow
- [ ] Consider a dedicated `EDITORIAL_GUIDE.md` for naming, uncertainty and source standards.
- [ ] Consider a Featured Media flag if the archive becomes large enough to need stronger curation.

### Future ideas
- [ ] Harbour snapshot cards combining AIS and photography.
- [ ] Yacht comparison cards.
- [ ] Continue refining gallery video identification and categorisation.

## Deferred

None currently.

## Blocked

None currently.

## Won’t implement

None currently.

## Completed

### v2.6.2
- [x] Refined the recovered cave excursion location to **Likely Blue Cave, Biševo, Croatia**.
- [x] Preserved the cave clip as an undated season highlight because the exact date/location remain unconfirmed by Cameron and Sophie.
- [x] Used the 13 July Biševo route loop as supporting evidence without adding a separate yacht stop.

### v2.6.1
- [x] Fixed the version source that was causing releases to revert to `2.2.0`.
- [x] Removed hard-coded `2.2.0` values from dashboard publishing scripts.
- [x] Updated country statistics to count **Countries visited** rather than underway transit countries.
- [x] Confirmed Albania is only present on an underway marker and no longer counts as visited.
- [x] Removed the stale VesselFinder/AIS image file from source media.
- [x] Added the recovered Kablin Bay aft-deck photo.
- [x] Added the Michelle snorkelling accident photo and Sakarun beach setup photo.
- [x] Added the dolphin **Music Edit** as a variant of the existing dolphin encounter.
- [x] Added the cave excursion as an undated Crew Life highlight.
- [x] Added the onboard CCTV deck-mishap clips as undated Crew Life highlights.
- [x] Added the Zadar Anchorage owner’s guest transfer entry.
- [x] Completed the Lapatica Bay / Kablin Bay naming consistency fixes.

### v2.6.0
- [x] Added grouped unified search across the journal, route, gallery and contextual content.
- [x] Added bidirectional Journal ↔ Map navigation using confirmed route-stop relationships.
- [x] Added the Antiquus Sushi & More evening in Zadar.
- [x] Added Toni’s dockside accident using confirmed details only, without asserting which arm was fractured.

### v2.5.4
- [x] Created a scalable SVG wordmark inspired by the lettering carried on Juno’s 7.
- [x] Converted the lettering to vector paths so the site does not depend on a local or commercial font.
- [x] Replaced the homepage text heading with the new accessible SVG wordmark.
- [x] Added responsive sizing and subtle shadow treatment for desktop and mobile.
- [x] Added the complete branch, build, test, merge, tag and cleanup commands to the release notes.

### v2.5.3
- [x] Added ROADMAP.md as the shared release checklist and backlog.
- [x] Added Cameron’s dawn photograph and “Good night” context at Levrnaka.
- [x] Expanded the 18 July Žut story with Konoba Vison, “Scampi – 1, Soph – 0” and Strawberry the donkey.
- [x] Renamed route and journal locations to place-first names, including **Levrnaka Bay** and **Žut Harbour**.
- [x] Added Reposado as a notable encounter in Zadar.
- [x] Added published charter guides to Reposado and Black Pearl.

### v2.5.2
- [x] Added concise Voyage Stop entries for Levrnaka and Žut.
- [x] Kept routine underway positions map-only.

### v2.5.1
- [x] Restored the garage tender and quayside photographs.
- [x] Corrected the satellite imagery endpoint.

## Release validation checklist

### Scope
- [x] ROADMAP reviewed and release scope confirmed.
- [x] Incomplete work explicitly deferred or blocked.

### Content
- [x] New journal wording reviewed against Cameron and Sophie’s messages.
- [x] Dates, chronology and locations checked.
- [x] Local spelling and geographical terminology checked.
- [x] Charter figures recorded as guide prices plus expenses.

### Media
- [x] Every new media ID resolves to an existing file.
- [x] Journal-to-gallery relationships checked.
- [x] Captions and categories reviewed.

### Technical
- [x] VERSION and release name updated.
- [x] Site build completed successfully.
- [x] Journal, gallery, voyage map and version data sanity-checked.
- [x] Changed-files ZIP created.
- [x] SHA256 generated.
