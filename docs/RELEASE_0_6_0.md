# Release 0.6.0 — Tracker Foundation

## Added

- Vessel IDs for JUNOS 7 and SETE
- Tracker config
- Provider-neutral tracker script
- Hourly GitHub Actions workflow
- Latest and archive AIS data structure
- Tracker documentation
- Site tracker data feed

## Apply

Copy this release over the repository root.

Commit:

```text
Add tracker foundation
```

Push to GitHub.

Then go to:

```text
GitHub > Actions > Track Yachts > Run workflow
```

The first run will create/update tracker files, but live positions require a configured AIS provider.
