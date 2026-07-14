# Juno's 7 – Mediterranean Journal 2026

> Don't document the yacht. Document the memories.

This repository contains the source for an interactive and printable journal documenting Cameron and Sophie's first Mediterranean season working together aboard **Juno's 7**.

The project produces:

- an interactive journal website
- a voyage dashboard and route map
- a local Captain's Dashboard for publishing route updates
- a permanent, structured media archive
- source material for a future printed Collector's Edition

## Quick start

For the public journal, run a local web server from the repository root and open `docs/index.html`, or use the GitHub Pages deployment from `/docs`.

For route updates, launch:

```text
Start Captains Dashboard.bat
```

After source changes, rebuild the clean output with:

```bash
python tools/build_site.py
```

## Project structure

```text
content/                    Source journal, route and media-index content
docs/                       Source website and GitHub Pages output
site/                       Clean build copied from docs/
admin-input/                Latest and archived manual location updates
tools/                      Build, publishing, routing and media utilities
tracker/                    Experimental vessel-tracking utilities
collector/                  Future Collector's Edition workspace
archive/                    Preserved project material
```

## Version 2.3.1

Contextual Discovery adds a curated, source-backed layer of nearby stories tied to the yacht’s actual stops. Discoveries appear in matching journal chapters, on the voyage map and on a dedicated “What They Almost Missed” page.

The v2.3.1 visual polish separates the transparent hero mark from the square app icon and gives the mark greater presence. See `RELEASE_2_3_1.md`, `RELEASE_2_3_0.md` and `CONTEXTUAL_DISCOVERY.md`.

## Guiding principle

This is not primarily a yacht tracker. It is a family journal.

AIS positions, maps and statistics are used only to support the story of the season.

## GitHub Pages

Recommended setting:

- Repository: `Junos7Journal`
- Branch: `main`
- Folder: `/docs`
