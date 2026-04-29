#!/usr/bin/env bash
# Common shell helpers for kalman_soil_assimilation scripts.

set -euo pipefail

log_info() {
  printf '[INFO] %s\n' "$*"
}

log_warn() {
  printf '[WARN] %s\n' "$*" >&2
}

log_error() {
  printf '[ERROR] %s\n' "$*" >&2
}

fail() {
  log_error "$*"
  exit 1
}

require_command() {
  local command_name="$1"
  command -v "${command_name}" >/dev/null 2>&1 || fail "Required command not found: ${command_name}"
}

require_file() {
  local file_path="$1"
  [[ -f "${file_path}" ]] || fail "Required file not found: ${file_path}"
}

require_dir() {
  local dir_path="$1"
  [[ -d "${dir_path}" ]] || fail "Required directory not found: ${dir_path}"
}

require_var() {
  local var_name="$1"
  [[ -n "${!var_name:-}" ]] || fail "Required environment variable is not set: ${var_name}"
}

repo_root() {
  local script_dir
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  cd "${script_dir}/.." && pwd
}
