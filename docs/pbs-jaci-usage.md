# PBS and JACI Usage

This document describes the initial PBS workflow for `kalman_soil_assimilation`.

## Current scope

The current templates are validation templates. They are intended to check the repository environment and run the current minimal Kalman Filter example through a PBS batch job.

## Files

```text
configs/sites/jaci/env.sh
configs/sites/jaci/paths.sh
configs/sites/jaci/modules.sh
jobs/pbs/env_check.pbs
jobs/pbs/run_minimal_example.pbs
```

## Local validation before PBS

From the repository root:

```bash
bash scripts/env_check.sh
bash scripts/run_minimal_example.sh
```

## PBS submission

On a PBS system, from the repository root:

```bash
qsub jobs/pbs/env_check.pbs
qsub jobs/pbs/run_minimal_example.pbs
```

## Values that must be reviewed on JACI

Review and adjust:

- queue name;
- account or project name;
- walltime;
- memory;
- number of CPUs;
- module names;
- scratch, work and output paths;
- MONAN and JEDI root paths.

## Design note

The PBS templates call scripts from `scripts/`. They should not contain scientific logic. Site-specific values should remain under `configs/sites/jaci/`.
