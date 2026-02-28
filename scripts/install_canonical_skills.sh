#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MAP_FILE="${ROOT_DIR}/canonical_skills.json"
TARGET_DIR="${1:-${CODEX_HOME:-$HOME/.codex}/skills}"

if [[ ! -f "${MAP_FILE}" ]]; then
  echo "error: canonical map not found: ${MAP_FILE}" >&2
  exit 1
fi

CANONICAL_SKILLS="$(python3 - "${MAP_FILE}" <<'PY'
import json, sys
path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    data = json.load(f)
for item in data.get("canonical_skills", []):
    name = str(item.get("name", "")).strip()
    if name:
        print(name)
PY
)"

PROTECTED_SKILLS="$(python3 - "${MAP_FILE}" <<'PY'
import json, sys
path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    data = json.load(f)
for item in data.get("protected_non_module_skills", []):
    name = str(item).strip()
    if name:
        print(name)
PY
)"

DEPRECATED_SKILLS="$(python3 - "${MAP_FILE}" <<'PY'
import json, sys
path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    data = json.load(f)
for item in data.get("deprecated_skills", []):
    name = str(item).strip()
    if name:
        print(name)
PY
)"

mkdir -p "${TARGET_DIR}"

while IFS= read -r skill; do
  [[ -z "${skill}" ]] && continue
  src="${ROOT_DIR}/${skill}"
  dst="${TARGET_DIR}/${skill}"
  if [[ ! -d "${src}" ]]; then
    echo "error: canonical skill dir missing: ${src}" >&2
    exit 1
  fi
  mkdir -p "${dst}"
  rsync -a --delete "${src}/" "${dst}/"
  echo "synced ${skill}"
done <<< "${CANONICAL_SKILLS}"

cp "${ROOT_DIR}/README.md" "${TARGET_DIR}/README.md"
cp "${MAP_FILE}" "${TARGET_DIR}/canonical_skills.json"

while IFS= read -r skill; do
  [[ -z "${skill}" ]] && continue
  path="${TARGET_DIR}/${skill}"
  if [[ -e "${path}" ]]; then
    rm -rf "${path}"
    echo "removed deprecated ${skill}"
  fi
done <<< "${DEPRECATED_SKILLS}"

shopt -s nullglob
for path in "${TARGET_DIR}"/linx-*; do
  skill="$(basename "${path}")"
  keep=0
  while IFS= read -r k; do
    [[ -z "${k}" ]] && continue
    if [[ "${k}" == "${skill}" ]]; then keep=1; break; fi
  done <<< "${CANONICAL_SKILLS}"
  if [[ "${keep}" -eq 0 ]]; then
    while IFS= read -r k; do
      [[ -z "${k}" ]] && continue
      if [[ "${k}" == "${skill}" ]]; then keep=1; break; fi
    done <<< "${PROTECTED_SKILLS}"
  fi
  if [[ "${keep}" -eq 0 ]]; then
    rm -rf "${path}"
    echo "removed non-canonical ${skill}"
  fi
done
shopt -u nullglob

echo "installed canonical skills into ${TARGET_DIR}"
