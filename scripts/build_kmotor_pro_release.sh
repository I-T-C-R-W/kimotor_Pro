#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGIN_DIR="$ROOT_DIR/kmotor_pro"
DIST_DIR="$ROOT_DIR/dist"
STAGE_DIR="$(mktemp -d /tmp/kmotor_pro_release_stage.XXXXXX)"

cleanup() {
  rm -rf "$STAGE_DIR"
}
trap cleanup EXIT

if [[ ! -f "$PLUGIN_DIR/metadata.json" ]]; then
  echo "plugin source tree missing: $PLUGIN_DIR" >&2
  exit 1
fi

VERSION="$(
  python3 - <<'PY' "$PLUGIN_DIR/metadata.json"
import json, sys
with open(sys.argv[1], "r", encoding="utf-8") as fh:
    data = json.load(fh)
print(data["release"]["version"])
PY
)"

mkdir -p "$DIST_DIR"
ARCHIVE="$DIST_DIR/KMotor_Pro-v${VERSION}.zip"
rm -f "$ARCHIVE"

mkdir -p "$STAGE_DIR/plugins" "$STAGE_DIR/resources"

cp "$PLUGIN_DIR/__init__.py" "$STAGE_DIR/plugins/"
cp "$PLUGIN_DIR/kmotor_pro_action.py" "$STAGE_DIR/plugins/"
cp "$PLUGIN_DIR/kmotor_pro_gui.py" "$STAGE_DIR/plugins/"
cp "$PLUGIN_DIR/kmotor_pro_linalg.py" "$STAGE_DIR/plugins/"
cp "$PLUGIN_DIR/kmotor_pro_solver.py" "$STAGE_DIR/plugins/"
cp "$PLUGIN_DIR/kmotor_pro_persist.py" "$STAGE_DIR/plugins/"
cp "$PLUGIN_DIR/kmotor_pro_24x24.png" "$STAGE_DIR/plugins/"
cp "$PLUGIN_DIR/kmotor_pro_24x24.png" "$STAGE_DIR/resources/icon.png"
cp "$PLUGIN_DIR/README.md" "$STAGE_DIR/plugins/"
cp "$PLUGIN_DIR/app.png" "$STAGE_DIR/plugins/"
cp "$PLUGIN_DIR/app2.png" "$STAGE_DIR/plugins/"

python3 - <<'PY' "$PLUGIN_DIR/metadata.json" "$STAGE_DIR/metadata.json"
import json
import sys

src = sys.argv[1]
dst = sys.argv[2]

with open(src, "r", encoding="utf-8") as fh:
    data = json.load(fh)

version = data["release"]["version"]
status = data["release"]["status"]
description = data["description"]
description_full = (
    "KMotor_Pro is a GPL-2.0-only KiCad 9 fork of KiMotor with "
    "deterministic routing, resistance stats, corner alignment helpers "
    "and safer geometry handling for PCB motor generation."
)

archive_metadata = {
    "$schema": "https://go.kicad.org/pcm/schemas/v1",
    "name": data["name"],
    "description": description[:150],
    "description_full": description_full,
    "identifier": data["identifier"],
    "type": "plugin",
    "author": {
        "name": data["author"]["name"],
        "contact": {
            "web": data["author"]["contact"]
        }
    },
    "maintainer": {
        "name": data["maintainer"]["name"],
        "contact": {
            "web": data["maintainer"]["contact"]
        }
    },
    "license": data["license"],
    "resources": {
        "homepage": data["homepage"]
    },
    "versions": [
        {
            "version": version,
            "status": status,
            "kicad_version": "9.0",
            "kicad_version_max": "9.99",
            "runtime": "swig"
        }
    ]
}

with open(dst, "w", encoding="utf-8") as fh:
    json.dump(archive_metadata, fh, indent=2)
    fh.write("\n")
PY

(
  cd "$STAGE_DIR"
  zip -r "$ARCHIVE" metadata.json plugins resources
)

echo "created: $ARCHIVE"
