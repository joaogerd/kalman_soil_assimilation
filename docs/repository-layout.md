# Repository Layout

This document summarizes the intended repository layout after the initial cleanup.

```text
kalman_soil_assimilation/
├── configs/
├── docs/
├── examples/
├── jobs/
├── kalman_soil/
├── scripts/
├── tests/
├── README.md
├── ROADMAP.md
├── requirements.txt
└── setup.py
```

## Directory responsibilities

- `kalman_soil/`: Python package code.
- `configs/`: site, experiment and example configuration files.
- `scripts/`: operational shell scripts.
- `jobs/`: batch-system job templates.
- `examples/`: minimal runnable examples.
- `tests/`: automated tests.
- `docs/`: technical documentation and design notes.

## Current phase decision

This phase only creates the structure. It does not move Python modules or redesign the public API. That keeps the branch small and reduces the risk of breaking the current prototype.
