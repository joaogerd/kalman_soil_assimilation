#!/usr/bin/env bash
# Environment modules for JACI PBS jobs.
# This file prepares the Python runtime used by validation jobs.

# Some site-provided Conda activation scripts reference variables that may be
# unset. Temporarily disable nounset while loading Anaconda and starting Conda,
# then restore it before returning to the repository scripts.
set +u

if command -v module >/dev/null 2>&1; then
  module load anaconda
else
  printf '[WARN] module command not available; skipping module setup.\n' >&2
fi

if command -v start_conda >/dev/null 2>&1; then
  start_conda
else
  printf '[WARN] start_conda command not available after loading anaconda.\n' >&2
fi

set -u

if command -v python >/dev/null 2>&1; then
  printf '[INFO] Python runtime: %s\n' "$(command -v python)"
else
  printf '[ERROR] Python command is not available after module setup.\n' >&2
  return 1 2>/dev/null || exit 1
fi
