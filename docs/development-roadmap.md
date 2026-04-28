# Development Roadmap

This document defines the incremental development path for `kalman_soil_assimilation`.

The project will evolve from a minimal Kalman Filter prototype into a lightweight scientific package for soil-moisture data assimilation and MONAN initial-condition generation.

## Principles

- Keep the architecture simple.
- Separate configuration from execution logic.
- Preserve scientific traceability.
- Use small branches and pull requests.
- Add tests before adding advanced algorithms.
- Avoid machine-specific paths in source code.

## Phases

1. Roadmap and documentation.
2. Architecture cleanup.
3. Modern shell scripts.
4. HPC job templates.
5. Runtime configuration.
6. Core scientific data model.
7. Kalman Filter hardening.
8. Observation operators.
9. Physical constraints and quality control.
10. MONAN input and output prototype.
11. External data readers.
12. Remapping.
13. End-to-end assimilation cycle.
14. Diagnostics and validation reports.
15. Advanced filters.

## Immediate next steps

The next branch should create the basic repository structure for configuration files, scripts, jobs, examples and tests while keeping the current package importable.
