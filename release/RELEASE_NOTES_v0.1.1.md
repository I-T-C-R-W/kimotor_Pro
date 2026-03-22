# KMotor_Pro v0.1.1

Error-fix release for the first public package.

## Fixes

- Fixed the release ZIP layout so `metadata.json` is placed at the archive root.
- This resolves KiCad's `invalid metadata.json` error during `Install from File`.

## Included feature set

- Radial default coil generation
- deterministic terminal and board text placement
- safer geometry handling
- resistance stats for total, phase, coil and ring values
- corner alignment helpers with NPTH hole arrays and silkscreen guides
