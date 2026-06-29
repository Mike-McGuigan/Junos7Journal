# Current Release

Version: 0.6.0

Name: Tracker Foundation

Build date: 2026-06-29 17:59:22 UTC

Status: Development / tracker scaffold

## Purpose

Adds the first automatic tracking framework for Juno's 7 and SETE.

This release does **not** yet include a guaranteed AIS data provider. It establishes the structure, workflow, vessel identifiers and output files needed for automatic tracking once a reliable source is configured.

## Vessels

- JUNOS 7 — IMO `1109712`, MMSI `319303300`
- SETE — MMSI `319314700`

## Highlights

- Adds `.github/workflows/track-yachts.yml`
- Adds `tracker/config.json`
- Adds `tracker/track_yachts.py`
- Adds latest-position JSON files
- Adds public site data file at `site/data/tracker.json`
- Adds tracker documentation

## What is needed to make this live

A position source must be configured. Options:

1. AIS API endpoint, preferred.
2. A reliable public endpoint that returns vessel position data.
3. Manual CSV/JSON imports until an automated source is available.

Do not commit usernames, passwords, API keys or VesselFinder credentials to the repo.
Use GitHub Actions secrets for anything private.
