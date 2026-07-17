# Gallery classification audit — v2.5.0

The gallery taxonomy is intentionally multi-label. `Crew Life` means the media records a crew member, their work, or a clearly crew-centred experience; it does not mean every scenic view sent by a crew member.

## Audit decisions

- Added **Crew Life** to `sundeck-black` because it records deck work.
- Added **Crew Life** to `teak-dent-repair` because it records Cameron's maintenance work.
- Removed **Crew Life** from `junos-marina`, which is primarily a yacht-at-berth image.
- Removed **Crew Life** from `dolphins-from-deck`, which is primarily wildlife and yacht context.
- Removed **Crew Life** from `rainy-start-to-shift`, which is primarily weather, anchorage and behind-the-scenes atmosphere.
- The underlying category key remains `crew` for compatibility; the visible label is now **Crew Life**.

Every media item remains classified in the canonical `content/media-index/media-index.json` file.
