# JACI Site Configuration

This directory contains site-specific configuration placeholders for running `kalman_soil_assimilation` on JACI-like PBS environments at INPE.

The files here are intentionally simple and should be reviewed on the machine before operational use.

## Files

- `env.sh`: general runtime variables.
- `modules.sh`: environment module commands.
- `paths.sh`: filesystem paths used by scripts and jobs.

## Rules

- Keep machine-specific values here, not inside Python modules.
- Keep scientific experiment settings in experiment configuration files.
- Treat placeholder values as examples until validated on JACI.
