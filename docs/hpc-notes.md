# HPC Notes

This document records the initial strategy for running the package in HPC environments.

## Goals

- Keep job templates simple.
- Keep site configuration outside Python code.
- Allow users to adjust queues, paths, modules and resources without editing package internals.
- Support future integration with MONAN and JEDI workflows.

## Recommended layout

```text
configs/sites/jaci/
├── env.sh
├── modules.sh
└── paths.sh

jobs/pbs/
├── assimilation.pbs
└── validation.pbs
```

## Variables to document

Site-specific configuration should document account, queue, walltime, nodes, tasks, threads, scratch directory, work directory, Python environment, modules, MONAN paths and optional JEDI paths.

## Current status

Validated job templates are not included yet. They will be added in a dedicated HPC support phase.
