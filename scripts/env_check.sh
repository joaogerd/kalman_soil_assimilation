#!/usr/bin/env bash
# Minimal environment checks.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

ROOT_DIR="$(repo_root)"

log_info "Checking repository environment"
log_info "Repository root: ${ROOT_DIR}"

require_command python
require_dir "${ROOT_DIR}/kalman_soil"
require_file "${ROOT_DIR}/kalman_soil/kalman_filter.py"
require_file "${ROOT_DIR}/requirements.txt"

log_info "Environment check completed successfully"
