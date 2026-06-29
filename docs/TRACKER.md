# Yacht Tracker

## Current status

The tracking framework is installed, but no live AIS provider is configured yet.

The tracker knows about:

| Vessel | IMO | MMSI | Role |
|---|---:|---:|---|
| JUNOS 7 | 1109712 | 319303300 | Main yacht |
| SETE | | 319314700 | Chase boat |

## Files

```text
tracker/config.json
tracker/track_yachts.py
.github/workflows/track-yachts.yml
data/ais/latest/
data/ais/archive/
site/data/tracker.json
```

## Running locally

```bash
python tracker/track_yachts.py
python tools/build_site.py
```

## GitHub Actions

The workflow is:

```text
.github/workflows/track-yachts.yml
```

It runs hourly and can also be triggered manually via **Actions > Track Yachts > Run workflow**.

## Important

This release does not include VesselFinder login automation or credential use.

Do not commit VesselFinder credentials, usernames, passwords, cookies or API tokens to GitHub.

If an AIS API or other source is used later, store keys in:

```text
GitHub repo > Settings > Secrets and variables > Actions
```

## Next step

Choose a data source.

Possible options:

1. Paid AIS API.
2. A public endpoint that returns position data.
3. Manual JSON/CSV import while the automated source is investigated.
