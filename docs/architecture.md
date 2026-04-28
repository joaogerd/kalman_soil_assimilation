# Architecture

## Current status

The current package contains a minimal Kalman Filter implementation and a small module layout:

```text
kalman_soil/
├── assimilation.py
├── data_loader.py
├── kalman_filter.py
├── model_state.py
└── visualization.py
```

This is a useful prototype, but it does not yet represent all concepts required for soil-moisture initial-condition generation.

## Target architecture

The package should remain small and explicit. The recommended structure is:

```text
kalman_soil/
├── core/
├── filters/
├── operators/
├── physics/
├── data/
├── remapping/
├── monan/
├── validation/
└── visualization/
```

## Core concepts

- State: soil moisture values by grid point and soil layer.
- Background: model state before assimilation.
- Observation: external measurement with value, location, time, depth, error and quality-control metadata.
- Observation operator: mapping from model state to observation space.
- Analysis: updated state after assimilation.
- Soil layer: vertical model layer with top and bottom depths.
- Grid: horizontal model or observation grid metadata.
- Uncertainty: background, process and observation error information.
- Initial-condition product: output file prepared for MONAN execution.

## Design decisions

The Kalman Filter core should remain independent from MONAN, SMAP, ASCAT or any other product. Product-specific logic belongs in readers, operators or adapters.

Operational scripts should live outside the Python package. Configuration files should be versioned and documented, but machine-specific values must remain easy to override.
