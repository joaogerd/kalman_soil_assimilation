#!/usr/bin/env bash
# Filesystem paths for JACI-like PBS environments.
# Replace placeholder values with validated paths on the target machine.

export KSA_PROJECT_ROOT="${KSA_PROJECT_ROOT:-$PWD}"
export KSA_WORK_DIR="${KSA_WORK_DIR:-$PWD/work}"
export KSA_OUTPUT_DIR="${KSA_OUTPUT_DIR:-$PWD/outputs}"
export KSA_LOG_DIR="${KSA_LOG_DIR:-$PWD/logs}"

# Optional future integration points.
export KSA_MONAN_ROOT="${KSA_MONAN_ROOT:-CHANGE_ME}"
export KSA_JEDI_ROOT="${KSA_JEDI_ROOT:-CHANGE_ME}"
