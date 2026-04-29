# PBS and JACI Usage

This document describes the initial PBS workflow for `kalman_soil_assimilation`.

## Current scope

The current templates are validation templates. They check the repository environment and run the current minimal Kalman Filter example through a PBS batch job.

## Files

```text
configs/sites/jaci/env.sh
configs/sites/jaci/paths.sh
configs/sites/jaci/modules.sh
jobs/pbs/env_check.pbs
jobs/pbs/run_minimal_example.pbs
```

## Observed JACI queues

The default queue in `configs/sites/jaci/env.sh` is `pesqmini`.

The queue `workq` was observed as disabled and should not be used as the default.

Observed enabled queues include:

- `aux`
- `pesqextra`
- `pesqhigh`
- `pesqmidi`
- `pesqmini`
- `oper`
- `preoper`
- `longtime`

## Local validation before PBS

From the repository root:

```bash
bash scripts/env_check.sh
bash scripts/run_minimal_example.sh
```

## PBS submission

On JACI, submit with an enabled queue. For a small validation job:

```bash
qsub -q pesqmini jobs/pbs/env_check.pbs
qsub -q pesqmini jobs/pbs/run_minimal_example.pbs
```

The queue may be changed later after checking the appropriate project policy.

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
