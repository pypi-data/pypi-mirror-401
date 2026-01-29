# Changelog

All notable changes to this project will be documented here.

## [1.6.0] - 2026-01-16
### Improved
- Abstract studio API calls via the APP SDK (SFD-312)
- Move extract config, update json config marker (SFD-242)
- Allow to use ISS in scripts (SFD-179)
- Allow to use input in uninstall scripts (SFD-200)
- Allow to rollback in case you leave interactive app creation (SFD-172)
- Add more documentation (SFD-172) 
- Allow to see in the cli why yaml is invalid (SFD-248)
- Replace (windows) line endings in application scripts (SFD-449)
- Support for `.appignore` file to exclude specified files and directories from app packaging. By default, all files are included unless listed in `.appignore`. (SFD-405)
- Make sure pipx pythonpath is found (SFD-438)
- Support locate service without port suffix

## [1.5.0] - 2025-09-17
### Improved
- SDK CLI: prompt user to upgrade software
- app upgrade: provide version information to/during migration
- SFD-204 fix stacktrace if timeout
- SFD-203 allow self signed cert
- FMG-3975 add schema ui plugin, remove prompt for version upgrade in dev

## [1.4.0] - 2025-09-02
### Improved
- Split library into scp-app-lib and scp-app-sdk, keeping only the SDK in this package (SFD-102)
- Improved SDK CLI code (SFD-99)

## [1.3.0] - 2025-08-05
### Added
- Support for UI plugins.

## [1.2.1] - 2025-07-09
### Fixed
- Script could not be executed (FMG-3876).

## [1.2.0] - 2025-05-07
### Improved
- Document the route that updates app configuration (FMG-3675).

## [1.1.0] - 2025-04-18
### Added
- `env` parameter in `create` CLI command (FMG-3376).
- Ability to set app version in manifest.
- Ability to add library in the app.

### Improved
- Review source code of build rendering.
- Review manifest generation issue with CLI.
- Improve docs for non-Python developers.
- Update README with detailed app creation/configuration instructions.
- Add input parameter to `run_uninstall` function.

### Fixed
- Issue retrieving template in CLI.
- Packaging issue with templating.
- API key not sent when publishing a new app.
- Git version check.
- Uninstall script execution by adding input parameter.

## [1.0.0] - 2025-02-05
### Added
- Validation schema for apps, builds, user apps, and app manifests (Marshmallow).
- API documentation of APP store (Tornado).
- CLI to manage apps — create, validate, build, and publish.
- Library to manage APP manifest.
- Library to manage CSFE.
- Library to validate manifest, apps, and runners.
- Library to manage builds.
- Icon support.
