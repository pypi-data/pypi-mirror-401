# CHANGELOG

## v1.0.0 (2026-01-03)

### Breaking Changes

* feat: Release v1.0.0 - Stable version with defunct APIs removed

The following services were removed because they are no longer provided by the official National Assembly Open API portal (returning 404/Error pages):
- `국회미래연구원_미래생각` (OT5EH10012030D12149)
- `국회미래연구원_미래서평` (OQX4LR0011965K19194)
- `의원연맹별_보조금_예산` (ONVQB00009257H12418)

Users should update their code to remove references to these `Service` enum members.

## v0.1.1 (2025-11-29)

### Chore

* chore: trigger release workflow test ([`76e5a26`](https://github.com/StatPan/assembly-api-client/commit/76e5a26680d1912c2df8cb6b4c5df8af2a86b542))

* chore: remove useless plan file ([`d6c1c3d`](https://github.com/StatPan/assembly-api-client/commit/d6c1c3de7f41a938ebb77e73298e7e12a542741b))

* chore: Remove legacy AssemblyMCP folder and fix linting ([`301bfee`](https://github.com/StatPan/assembly-api-client/commit/301bfee8365245e485cd40dd6d1d046b260921d6))

* chore: Setup pre-commit and ruff, update docs and config ([`9588492`](https://github.com/StatPan/assembly-api-client/commit/9588492a4e232b9c43e7d6a11a67dfe174c67293))

### Feature

* feat: add automated version management with python-semantic-release (#2)

- Configure PSR v9 with Angular commit parser
- Add version tracking for __init__.py and pyproject.toml
- Create GitHub Actions release workflow
- Enable automated PyPI publishing
- Sync version to 0.1.1 across files ([`64f9820`](https://github.com/StatPan/assembly-api-client/commit/64f98202b7a68bb95ad61258e9457ad1706b25b1))

* feat: enhance spec download error diagnostics

- Detect HTML error pages vs Excel files
- Provide detailed troubleshooting messages
- Include content preview in error for debugging
- Add specific guidance for common failure cases ([`5e5279b`](https://github.com/StatPan/assembly-api-client/commit/5e5279b3b251c6c4a0934fbef4c6edead4610977))

* feat: add automatic version bumping to update workflow

- Created scripts/bump_version.py to increment patch version
- Updated workflow to bump version on spec updates
- Version bumped to 0.1.1
- Each spec update will now automatically get a new version number ([`e34027a`](https://github.com/StatPan/assembly-api-client/commit/e34027a43a2a64ec196ebd86317a2a17049e68b9))

* feat: add service metadata support

- Added load_service_metadata() to load comprehensive metadata from all_apis.json
- Extended AssemblyAPIClient with service_metadata attribute
- Provides description, category, organization info for each service
- Enables richer service information in downstream tools (assemblymcp) ([`4578cdf`](https://github.com/StatPan/assembly-api-client/commit/4578cdfdfbebbd11d3994ce362d603833c9f8eae))

* feat: Initial commit with robust client, tests, and automation ([`5cd90cc`](https://github.com/StatPan/assembly-api-client/commit/5cd90cc5af77593574ea544f7c44d5d2fba81115))

### Fix

* fix: add automatic infSeq fallback for spec download (#1)

- Implement automatic retry with infSeq=1 when infSeq=2 fails
- Add detailed logging for fallback attempts
- Add integration test for service OS46YD0012559515463
- Improve error messages with context from both attempts
- Remove unused main.py sample file

Some services (e.g., OS46YD0012559515463) only support infSeq=1
while most newer services require infSeq=2. This fix makes the
client robust to both cases without requiring manual intervention. ([`fa9aec9`](https://github.com/StatPan/assembly-api-client/commit/fa9aec96cbfc17c2146e127a900f220c4182bd14))

### Refactor

* refactor: Improve errors.py and remove unused legacy models.py ([`15f13d0`](https://github.com/StatPan/assembly-api-client/commit/15f13d014201ebee2a1c3faa1d796effac908d34))
