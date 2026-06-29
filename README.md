# Juno's 7 – Mediterranean Journal 2026

> Don't document the yacht. Document the memories.

This repository contains the source for an interactive and printable journal documenting Cameron and Sophie's first Mediterranean season working together aboard **Juno's 7**.

The project is designed to produce:

- an interactive website
- a printable collector's edition
- a permanent media archive
- structured route and journal data

## Quick Start

Open:

```text
website/index.html
```

This is currently a static prototype and can be hosted directly with GitHub Pages.

## Project Structure

```text
docs/                       Project notes, roadmap and design documentation
website/                    Static interactive journal
journal/                    Source journal entries in Markdown
media/originals/            Untouched original photographs and videos
media/processed/            Web-optimised media
media/thumbnails/           Generated thumbnails
maps/                       Route and GeoJSON map data
print/                      Collector's edition and PDF layouts
tools/                      Future build/export utilities
archive/                    Source material and conversation notes
```

## Guiding Principle

This is not primarily a yacht tracker. It is a family journal.

AIS positions, maps and statistics are used only to support the story of the season.

## GitHub Pages

Recommended setting:

- Repository: `Junos7Journal`
- Branch: `main`
- Folder: `/website`

If GitHub Pages does not allow `/website` directly on your account, copy the contents of `website/` into `/docs` and publish from `/docs` instead.
