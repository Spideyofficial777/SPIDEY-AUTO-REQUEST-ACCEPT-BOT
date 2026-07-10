# Changelog

All notable changes to this project are documented in this file.

Starting with `v1.0.0`, every entry below this line is generated from the
project's real commit history by `.github/workflows/release.yml` and
`.github/workflows/monthly-maintenance.yml` — see `AUTOMATION.md` for how
that works. Nothing is added by hand.

## [v1.2.0] - 2026-07-10

## Highlights

- Update bot messages and interface text (759e6c2)
- Integrate modular group management plugins (6b9ed28)
- Add safe channel membership validation (fdbe0a4)

## New Features

- Update bot messages and interface text (759e6c2)
- Integrate modular group management plugins (6b9ed28)
- Add safe channel membership validation (fdbe0a4)
- Add owner-only leave command (6cfe0b1)
- Add private group management controls (ecef3ae)
- Add private command guidance (d913871)
- Add group management settings (952c76c)
- Add administrative tools (0e4210b)
- Add user reporting system (463fb60)
- Add anti-spam protection (bf376d5)
- Add anti-flood protection (710908e)
- Add configurable content locks (7a520f1)
- Add custom filters with media and buttons (c66ba50)
- Add persistent group notes (5c3b144)
- Add mute and temporary mute commands (c775803)
- Add ban and temporary ban commands (5beef88)
- Add warning management system (4429c6f)
- Add group moderation commands (f7fce26)
- Add customizable goodbye messages (ef30358)
- Add customizable welcome messages (2d9ec48)
- Add shared private group selector (7888905)
- Add persistent group discovery registry (48a9f59)
- Add shared group management helpers (9afe4e7)
- Initialize group management plugin package (aa85405)
- Add persistent group registry support (e9a1027)
- Add persistent group management storage (3513c08)

## Improvements

- Remove legacy group handlers (e8ba512)

## Bug Fixes

- Improve start flow and force-sub validation (69e524d)

## Documentation

- Update project documentation (278d220)
- Change git user for actions in readme-update.yml (8390c60)

## Internal Changes

- Update release.yml (7df322f)
- Update git identity in monthly maintenance workflow (a37c05f)

## Files Updated

- `.github/workflows/monthly-maintenance.yml`
- `.github/workflows/readme-update.yml`
- `.github/workflows/release.yml`
- `Script.py`
- `bot.py`
- `database/database.py`
- `database/group_db.py`
- `plugins/commands.py`
- `plugins/force_sub.py`
- `plugins/group.py`
- `plugins/group/__init__.py`
- `plugins/group/admin_tools.py`
- `plugins/group/antiflood.py`
- `plugins/group/antispam.py`
- `plugins/group/bans.py`
- `plugins/group/filters.py`
- `plugins/group/goodbye.py`
- `plugins/group/group_registry.py`
- `plugins/group/group_selector.py`
- `plugins/group/helpers.py`
- …and 12 more file(s)

## Contributors

- SPIDEY OFFICIAL
- Spideyofficial777

## [v1.1.0] - 2026-07-03

## Highlights

- Add release automation and version management (0cca38c)

## New Features

- Add release automation and version management (0cca38c)

## Documentation

- Refresh README metadata for v1.0.15 [skip ci] (d04576a)
- Update changelog for v1.0.15 [skip ci] (ad6f179)
- Refresh README metadata for v1.0.14 [skip ci] (32e767d)
- Update changelog for v1.0.14 [skip ci] (d806605)
- Refresh README metadata for v1.0.13 [skip ci] (38b5985)
- Update changelog for v1.0.13 [skip ci] (57fec47)
- Update changelog for v1.0.12 [skip ci] (6249447)
- Refresh README metadata for v1.0.11 [skip ci] (c6cfe81)
- Update changelog for v1.0.11 [skip ci] (634cc32)
- Refresh README metadata for v1.0.10 [skip ci] (c51a0ac)
- Update changelog for v1.0.10 [skip ci] (4114188)
- Refresh README metadata for v1.0.9 [skip ci] (5efb055)
- Update changelog for v1.0.9 [skip ci] (2243cdc)

## Internal Changes

- SPIDEY-AUTO-REQUEST-ACCEPT-BOT (c949106)
- SPIDEY-AUTO-REQUEST-ACCEPT-BOT (e9f9aec)
- Update git email configuration in release workflow (dc421a7)
- Update git user email in workflow configuration (3107824)
- Update git user email in workflow configuration (cf93fb8)
- SPIDEY-AUTO-REQUEST-ACCEPT-BOT (38b4550)
- SPIDEY-AUTO-REQUEST-ACCEPT-BOT (89325d5)
- Update git identity in release workflow (c3f9a82)
- SPIDEY-AUTO-REQUEST-ACCEPT-BOT (ed9f79d)
- SPIDEY-AUTO-REQUEST-ACCEPT-BOT (f7bd6f5)
- SPIDEY-AUTO-REQUEST-ACCEPT-BOT (8d3a200)
- SPIDEY-AUTO-REQUEST-ACCEPT-BOT (71e521d)
- SPIDEY-AUTO-REQUEST-ACCEPT-BOT (5df7467)
- SPIDEY-AUTO-REQUEST-ACCEPT-BOT (cad5c9d)
- SPIDEY-AUTO-REQUEST-ACCEPT-BOT (f9b1158)
- SPIDEY-AUTO-REQUEST-ACCEPT-BOT (4a4326f)

## Files Updated

- `.github/S`
- `.github/scripts/S`
- `.github/scripts/analyze-commits.sh`
- `.github/scripts/bump-configs-version.sh`
- `.github/scripts/read-configs-version.sh`
- `.github/scripts/render-notes.sh`
- `.github/workflows/monthly-maintenance.yml`
- `.github/workflows/readme-update.yml`
- `.github/workflows/release.yml`
- `Script.py`
- `configs.py`

## Contributors

- SPIDEY OFFICIAL
- spideyofficial777

## [v1.0.0] - Baseline

Initial tracked release. Established the current feature set: request
auto-accept, multi-channel force-subscribe, CAPTCHA join protection,
welcome/leave messaging, admin commands (`/stats`, `/users`, `/broadcast`,
`/ban`, `/unban`), and MongoDB-backed persistence.
