#!/usr/bin/env bash
# Run the current minimal Kalman Filter example.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

ROOT_DIR="$(repo_root)"

log_info "Running minimal Kalman Filter example"
cd "${ROOT_DIR}"

require_command python
require_file "${ROOT_DIR}/kalman_soil/kalman_filter.py"

python "${ROOT_DIR}/kalman_soil/kalman_filter.py"

log_info "Minimal example completed successfully"
