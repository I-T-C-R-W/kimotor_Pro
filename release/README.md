# Release Tree

This directory contains the installable plugin layout for `KMotor_Pro`.

## Folder

- `com_github_itcrw_kmotor_pro/`

This folder is the one that should go into the release ZIP for KiCad installation.

## Build

Run:

```bash
./scripts/build_kmotor_pro_release.sh
```

This creates:

- `dist/KMotor_Pro-v<version>.zip`

The ZIP contains only the release plugin folder, not the full development workspace.
