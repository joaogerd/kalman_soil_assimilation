#!/usr/bin/env bash
# Environment modules for JACI-like systems.
# Replace these placeholders with the validated module stack on JACI.

if command -v module >/dev/null 2>&1; then
  module purge
  # module load python/3.11
  # module load netcdf
else
  printf '[WARN] module command not available; skipping module setup.\n' >&2
fi
