# Kalman Soil Assimilation

Kalman Soil Assimilation is a Python package under development for soil moisture data assimilation and land-surface initial-condition generation for MONAN.

The project starts from a simple Kalman Filter implementation and is being evolved into a lightweight, reproducible and operationally useful scientific tool for generating soil-water initial conditions from model backgrounds, observations and satellite products.

## Scientific goal

The main goal is to estimate physically consistent soil moisture fields by combining:

- MONAN or external model background fields;
- satellite soil-moisture products such as SMAP, ASCAT, GLDAS and ERA5-Land;
- optional in situ observations;
- observation operators that map model soil layers to observation space;
- background, process and observation uncertainty estimates;
- physical constraints such as saturation, wilting point, land-sea mask and soil-layer limits.

The first target variable is soil moisture, but the architecture must remain extensible for other land-surface variables.

## Current status

The repository currently contains a minimal Kalman Filter prototype and an initial package layout. It is not yet a complete MONAN initial-condition generator.

The active development plan is documented in:

- [ROADMAP.md](./ROADMAP.md) - current roadmap file;
- [docs/development-roadmap.md](./docs/development-roadmap.md) - phased technical roadmap;
- [docs/architecture.md](./docs/architecture.md) - recommended package architecture;
- [docs/jaci-pbs.md](./docs/jaci-pbs.md) - initial guidance for JACI/PBS usage;
- [docs/configuration.md](./docs/configuration.md) - configuration strategy.

## Existing package layout

```text
kalman_soil/
├── __init__.py
├── assimilation.py
├── data_loader.py
├── kalman_filter.py
├── model_state.py
└── visualization.py
```

This layout is intentionally small. The next development phases will reorganize the package incrementally, avoiding a heavy framework while adding the concepts needed for real soil-moisture assimilation.

## Installation

For the current prototype:

```bash
git clone https://github.com/joaogerd/kalman_soil_assimilation.git
cd kalman_soil_assimilation
pip install -r requirements.txt
```

A future phase will migrate packaging to `pyproject.toml` and add optional dependency groups for development, visualization, satellite products and HPC workflows.

## Minimal Kalman Filter example

```python
from kalman_soil.kalman_filter import KalmanFilter
import numpy as np

state_dim = 2
obs_dim = 1

kf = KalmanFilter(state_dim, obs_dim)
kf.set_observation_matrix(np.array([[1.0, 0.5]]))
kf.set_state_transition(np.eye(state_dim))
kf.set_process_covariance(np.eye(state_dim) * 0.01)
kf.set_observation_covariance(np.eye(obs_dim) * 0.1)

z = np.array([[0.9]])

kf.predict()
kf.update(z)

print(kf.get_state())
```

## Development principles

- Keep the architecture simple and explicit.
- Separate configuration from execution logic.
- Preserve scientific traceability.
- Prefer small, reviewable branches and pull requests.
- Add tests before increasing algorithmic complexity.
- Avoid hidden hardcoded paths, machine names or queue settings.
- Support HPC use cases without turning the package into a heavy workflow framework.

## License

This repository currently declares the Creative Commons Attribution-NonCommercial 3.0 Unported license. Because this is a software package, the license should be reviewed in a future governance phase and aligned with the intended software distribution policy.

## Author

João Gerd Zell de Mattos
