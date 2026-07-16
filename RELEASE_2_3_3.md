# Juno's 7 Journal v2.3.3 — Media Linking Fix

This corrective patch fixes missing media panels for the 14 July Komiža dawn and 15 July Smokvica storm entries.

## Fix

`docs/data/journal.json` contains an embedded media catalogue used by the journal and gallery. The two new photos had been added to the canonical media index and copied into the media folders, but were not included in that embedded catalogue.

The build now synchronises the embedded catalogue from `docs/data/media.json` every time `tools/build_site.py` runs, preventing the two sources from drifting apart again.

## Apply

Extract the patch over the repository root and run:

```bash
python tools/build_site.py
```
