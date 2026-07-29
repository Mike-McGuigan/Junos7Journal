# Changelog

## 2.7.4 - Dashboard Safety Guards

- Added Captain's Dashboard server checks so `localhost:8765` refuses to start if it is already being served from a different repository folder.
- Added a clear dashboard error when port `8765` is already occupied by a non-dashboard process.
- Displayed the active dashboard version, release title, branch, working-tree state and serving repository root in the dashboard health panel.
- Removed duplicate repository output from the dashboard starter.
- Removed the non-actionable credential-helper warning from the visible dashboard health checklist.
- Updated local save confirmations so they include the repository path being written to.
- Improved route-update filename sanitising so passage names such as `Crotone -> Valletta` become clean `crotone-to-valletta` filenames.
- Prevented stale dashboard JavaScript from being reused after a rebuild by adding local no-cache headers and a versioned admin script URL.
- Improved the manual sea-waypoint editor so the base route is removed while a leg is being edited, leaving only the selected cyan editable leg and avoiding the appearance of a duplicate/new route.
- Fixed manual sea-waypoint numbering so clicks are added in placement order instead of being reordered by nearest route segment.
- Updated version and build metadata to `2.7.4`.

## 2.7.3 - Route Editor Leg Fix

- Fixed the Voyage Route Editor so zero-distance duplicate route points are labelled as same-position legs and are not opened for manual waypoint editing.
- Changed the route leg selector to default to the latest non-zero leg.
- Updated waypoint editing so new clicks are inserted into the nearest segment of the active leg instead of always being appended to the end.
- Kept the active leg highlighted as a blue dashed line while editing.
- Updated version and build metadata to `2.7.3`.

## 2.7.2 - Flavour Card Food Images

- Added optional image support to **Flavour of the place** journal cards.
- Added illustrative regional food images for the Greek island, Dalmatian seafood and Calabrian flavour cards.
- Reused existing real journal food photos for the Zut scampi and Zadar sushi flavour cards.
- Labelled generated food assets as illustrative so they remain distinct from Cameron and Sophie's own media.
- Updated version and build metadata to `2.7.2`.

## 2.7.1 — Crotone Arrival and Dashboard Save Flow

- Added the 26 July arrival at **Crotone Old Harbour, Calabria, Italy**.
- Added Crotone contextual discovery for ancient Kroton, Pythagoras and Capo Colonna.
- Added **Flavour of Calabria** to the Crotone journal entry.
- Confirmed Italy is counted in **Countries visited** now that Juno’s 7 has made a confirmed Italian stop.
- Renamed the Captain's Dashboard new-position action from **Publish** to **Save Route Update**.
- Changed the dashboard save flow so it saves and rebuilds locally without committing or pushing automatically.
- Refreshes the dashboard tab after successful local route-update saves.
- Updated version and build metadata to `2.7.1`.

## 2.7.0 — Voyage Playback and Map Usability

- Added distance-spaced directional arrows along the rendered voyage route geometry.
- Centred the directional route arrows on the plotted line.
- Limited map zoom levels and disabled horizontal world wrapping.
- Added voyage playback controls with play/pause, progress scrubber, five speed levels and optional map following.
- Added an extra-slow playback speed.
- Playback follows manual sea waypoints so curved routes and crossings match the plotted track.
- Added active route-point highlighting during playback.
- Moved selected route-point detail cards beside the map on larger screens.
- Updated the Captain's Dashboard functional panels to behave as a single-open accordion.
- Scroll newly opened Captain's Dashboard panels into view.
- Updated the Captain's Dashboard new-position form so the date defaults to the current date and the location name starts empty with placeholder text.
- Preserved the v2.6.3 route-points/passages statistics separation.
- Updated version and build metadata to `2.7.0`.

## 2.6.3 — Passage Statistics Refinement

- Changed longest and average passage calculations so underway/AIS transit markers no longer split continuous passages.
- Kept all route nodes visible on the voyage map while calculating passage statistics between real stops and anchorages.
- Updated dashboard wording from route legs to passages for the average passage tile.
- Renamed the homepage metric from **Longest leg** to **Longest passage**.
- Renamed **Route stops** to **Route points** to reflect that the map includes underway markers and other plotted positions.
- Updated version and build metadata to `2.6.3`.

## 2.6.2 — Cave Location Refinement

- Updated the recovered cave excursion from a generic Croatian Adriatic location to **Likely Blue Cave, Biševo, Croatia**.
- Preserved the entry as an undated season highlight because Cameron and Sophie have not directly confirmed the exact cave or date.
- Added the 13 July Vis-to-Komiža route loop towards Biševo as supporting context without creating a false yacht stop.
- Updated version and build metadata to `2.6.2`.

## 2.6.1 — Maintenance & Editorial Consistency

- Fixed the recurring version downgrade by removing hard-coded `2.2.0` values from the manual-location publishing tools.
- Set the authoritative root `VERSION` source to `2.6.1` and aligned generated version metadata through the normal build.
- Changed the dashboard/home metric from **Countries** to **Countries visited**.
- Updated route statistics so underway transit markers do not count as visited countries; Albania remains a transit point only.
- Synced the legacy embedded route copy inside `journal.json` during builds to avoid stale country/location data.
- Removed the uncatalogued VesselFinder/AIS image file from the source media folder.
- Added the recovered Kablin Bay aft-deck photograph, Sakarun beach setup photograph and Michelle snorkelling accident photograph.
- Added the dolphin **Music Edit** as a variant of the existing bow-dolphin encounter rather than a separate sighting.
- Added the cave excursion and onboard CCTV deck-mishap clips as undated Crew Life / season-highlight entries.
- Added the 24 July Zadar Anchorage guest-transfer entry.
- Completed the Lapatica Bay / Kablin Bay naming consistency fixes across journal, route and geometry data.

## 2.6.0 — Navigation & Discovery

- Added grouped unified search across journal entries, route locations, gallery captions, discoveries, Did You Know, Flavour and notable encounters.
- Added reusable-tab Journal → Map navigation and Map → Journal links.
- Added the 20 July Antiquus Sushi & More evening and Toni’s dockside accident in Zadar.
- Kept the accident entry factual and left the injured arm unspecified.


## v2.5.4 — Authentic Yacht Wordmark

- Added `docs/assets/icons/junos7-wordmark.svg`, an outlined vector wordmark inspired by the yacht’s real hull lettering.
- Updated the homepage hero to use the SVG wordmark while preserving accessible alternative text.
- Added responsive wordmark sizing and presentation styling.
- Added a complete release-specific Git workflow to `RELEASE_2_5_4.md`.

## 2.4.1 — Gallery Classification Fix

- Makes gallery categories part of the canonical media index so later publishes preserve them.
- Corrects category assignments for the Cavtat passage, Black Pearl and Smokvica media.
- Removes the unsupported claim that SETE is visible in the Cavtat passage photograph.
- Standardises current journal, route and dashboard wording from “under way” to “underway”.
- Rebuilds and validates the generated site as version 2.4.1.

## 2.3.1 - Contextual Discovery Polish

- Separated the on-page hero mark from the square app/favicon icon.
- Made the hero Juno’s 7 artwork transparent so the live header gradient shows through without a mismatched tile.
- Increased the hero mark substantially and tightened the artwork inside its canvas for stronger visual presence.
- Retained the approved rounded-square logo for browser and installed-app icons.

## 2.3.0 - Contextual Discovery

- Added a curated, source-backed discovery layer tied to exact route stops.
- Added eight initial discoveries selected by proximity, significance and connection to the actual voyage.
- Added discovery cards to matching journal chapters and a dedicated discovery page.
- Added discovery markers, badges and selected-stop context to the voyage dashboard.
- Added build-time validation for route matching, journal matching, distance policy and source URLs.
- Documented the editorial rule that no discovery is better than forced trivia.

## 2.2.2 - Journal Experience Polish

- Identified Kos immediately in the opening chapter and changed its displayed location to Kos, Greece.
- Rebuilt the supplied Juno’s 7 logo with the exact site navy and removed white corner/rim artefacts.
- Removed gallery-card ivory gaps and corner slivers by using a complete navy card surface.
- Increased gallery title contrast and strengthened description weight and readability.
- Restored the lightweight changed-files patch workflow for point releases.

## 2.2.1 - Journal Experience Patch

- Replaced the incorrect mark with the approved Juno’s 7 yacht logo supplied by Mike, including the ivory monogram, gold bow accent and wake.
- Added a remembered Oldest → Newest / Newest → Oldest journal-order toggle.
- Kept the latest chapter featured at the top and retained it in the full journal with a Latest badge.
- Honoured explicit entry media order, placing the rainy video before the clearer-weather photograph in “Much Nicer”.
- Added the 13 July roundabout passage towards Biševo and back to Komiža.
- Added Cameron and Sophie’s two dolphin-at-the-bow videos, including the owner’s child’s delighted reaction.
- Updated route, dashboard, journal, media and build metadata to v2.2.1.

## 2.2.0 - Journal Experience

- Rebuilt the public journal as a magazine-style chapter experience.
- Added structured Crew Moment, Did You Know?, Flavour and Notable Encounter sections.
- Added uncropped story media, cropped gallery browsing and a full-screen media viewer.
- Added non-destructive enhanced-media support and selected enhanced working copies.
- Added Juno’s 7 favicon branding and responsive polish across the site.
- Enabled mouse-wheel map zoom and improved voyage-map exploration.
- Standardised Underway / Moored / At anchor terminology and date labels.
- Preserved and aligned the supplied route and manual voyage geometry through Vis.
- Added the complete re-provided July media set: Black Pearl, Pakleni, the night shift, dolphins off Milna, teak repair, Vis sunset/ash, changing weather, Cameron working aloft and the afternoon off.
- Expanded the journal to 22 chapters and 38 indexed media items.

## 2.1.1 - Geographic Intelligence polish

- Display enriched location metadata on the Captain's Dashboard admin map popups.
- Treat missing global Git credential helper as optional information, not a red health-check failure.
- Update version metadata to 2.1.1.

## 2.1.0 - Geographic Intelligence

- Added publish-time reverse geocoding.
- Added friendly location metadata to route and dashboard data.

### 2.3.3 - Media Linking Fix
- Synchronises the embedded journal media catalogue with the canonical media index during every site build.
- Restores the Komiža dawn and Smokvica storm photographs in the journal and gallery.

## 2.5.0 — Connected Storytelling
- Audited all 42 gallery records and clarified the Crew Life taxonomy.
- Added visible category badges and links from gallery media back to related journal chapters.
- Labelled chapter media and persisted media-to-entry relationships in canonical data.
- Added discovery category filtering and direct links to journal chapters and the voyage map.
- Added longest passage, average passage, leg count and countries visited to route statistics.
