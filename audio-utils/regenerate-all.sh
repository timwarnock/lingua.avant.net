#!/bin/bash
set -euo pipefail

BASE_DIR="ora/docs"
GENERATOR="python audio-utils/generate-rosary-audio.py"

TIMINGS_ONLY=""
LANGUAGES=()

usage() {
  cat <<EOF
Usage: $(basename "$0") [options]

Regenerate audio (or just timings) for all compatible prayer JSON files
using GNU parallel.

Options:
  --language <lang>   Limit to this language (can be repeated)
  --timings-only      Pass --timings-only to the generator (only updates JSON timing data)
  -h, --help          Show this help

By default processes every language except audio-testing, assets, stylesheets.
Finds all *.json that contain a "passages" key.
EOF
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --language)
      if [[ $# -lt 2 ]]; then
        echo "Error: --language requires an argument" >&2
        usage
      fi
      LANGUAGES+=("$2")
      shift 2
      ;;
    --timings-only)
      TIMINGS_ONLY="--timings-only"
      shift
      ;;
    -h|--help)
      usage
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      ;;
  esac
done

if ! command -v parallel >/dev/null 2>&1; then
  echo "Error: GNU parallel is required but not found." >&2
  echo "Install e.g. with: sudo apt install parallel" >&2
  exit 1
fi

# Determine dirs to scan
if [ ${#LANGUAGES[@]} -eq 0 ]; then
  mapfile -t LANG_DIRS < <(find "$BASE_DIR" -mindepth 1 -maxdepth 1 -type d     ! -name 'audio-testing' ! -name 'assets' ! -name 'stylesheets' | sort)
else
  LANG_DIRS=()
  for lang in "${LANGUAGES[@]}"; do
    d="$BASE_DIR/$lang"
    if [ -d "$d" ]; then
      LANG_DIRS+=("$d")
    else
      echo "Warning: no directory for language '$lang'" >&2
    fi
  done
fi

if [ ${#LANG_DIRS[@]} -eq 0 ]; then
  echo "No directories to process."
  exit 0
fi

# Collect all compatible JSONs
JSONS=()
for d in "${LANG_DIRS[@]}"; do
  while IFS= read -r -d '' json; do
    if grep -q '"passages"' "$json" 2>/dev/null; then
      JSONS+=("$json")
    fi
  done < <(find "$d" -name "*.json" -print0 | sort -z)
done

echo "Found ${#JSONS[@]} compatible JSON file(s) to process."

if [ ${#JSONS[@]} -eq 0 ]; then
  echo "Nothing to do."
  exit 0
fi

echo "Launching with GNU parallel (-j 4) ..."
echo "Each job: $GENERATOR <json> $TIMINGS_ONLY"
echo

parallel --progress --eta -j 4   "$GENERATOR" {} $TIMINGS_ONLY   ::: "${JSONS[@]}"

echo
echo "Done."
