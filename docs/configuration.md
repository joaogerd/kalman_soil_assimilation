# Configuration Strategy

The project should separate scientific configuration from execution logic.

## Configuration categories

Recommended categories:

- experiment metadata;
- input background file;
- observation files;
- soil-layer definitions;
- grid and remapping options;
- uncertainty settings;
- physical constraints;
- output paths;
- diagnostics.

## Site-specific configuration

Machine-specific settings must be placed under `configs/sites/<site-name>/`.

Examples:

```text
configs/sites/jaci/
├── env.sh
├── modules.sh
└── paths.sh
```

These files should define paths, module names, queues and resource defaults. They should not contain scientific logic.

## Experiment configuration

Experiment files should live under `configs/experiments/` or `configs/examples/`.

A minimal experiment should define:

- valid time;
- background file;
- observation source;
- target variable;
- soil layers;
- output directory;
- diagnostics to generate.

## Rules

- Do not hardcode local paths in Python modules.
- Do not hardcode queue names in scripts.
- Document every required variable.
- Prefer explicit defaults over implicit behavior.
