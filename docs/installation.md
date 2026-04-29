# Installation

This document describes the initial installation workflow for `kalman_soil_assimilation`.

## Basic installation

From the repository root:

```bash
python -m pip install -r requirements.txt
```

For editable development mode:

```bash
python -m pip install -e .
```

## Initial dependencies

The initial scientific Python dependencies are:

- `numpy`
- `scipy`
- `matplotlib`
- `xarray`
- `netCDF4`
- `pandas`

These dependencies support the current Kalman Filter prototype and prepare the package for NetCDF-based model and observation data handling.

## Validation

After installation, run:

```bash
bash scripts/env_check.sh
bash scripts/run_minimal_example.sh
```

On JACI, use the PBS validation workflow documented in `docs/pbs-jaci-usage.md`.
