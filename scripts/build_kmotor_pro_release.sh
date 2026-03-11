#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGIN_DIR="$ROOT_DIR/release/com_github_itcrw_kmotor_pro"
DIST_DIR="$ROOT_DIR/dist"

if [[ ! -f "$PLUGIN_DIR/metadata.json" ]]; then
  echo "release tree missing: $PLUGIN_DIR" >&2
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

(
  cd "$PLUGIN_DIR"
  zip -r "$ARCHIVE" .
)

echo "created: $ARCHIVE"
