# KMotor_Pro v0.1.0

First stable release of the KiCad 9 fork, continued from KiMotor and extended as `KMotor_Pro`.

## Highlights

- Radial coil generation is now the default release path.
- Deterministic board text and terminal reference placement.
- Safer geometry handling for vertical and near-vertical intersection cases.
- Generated GND and mask zones are replaced without deleting unrelated user zones.
- Expanded resistance stats for total, phase, coil and ring values.
- Corner alignment helpers with NPTH hole arrays plus silkscreen angular scales.
- KiCad 9-aware footprint path detection.
- Reworked GUI layout with more stable column sizing and clearer status feedback.

## Included in this release

- `KMotor_Pro` fork workspace under `kmotor_pro/`
- installable release tree under `release/com_github_itcrw_kmotor_pro/`
- release ZIP builder script: `scripts/build_kmotor_pro_release.sh`

## Known scope

- `3P` is the primary stable target in this release.
- `1P` is improved and usable.
- `3P+N` still needs a final dedicated neutral-routing topology.
