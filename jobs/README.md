# Jobs

This directory will contain job templates for HPC batch systems.

Initial focus:

- PBS templates for JACI-like environments;
- simple validation jobs;
- clear placeholders for queue, account, walltime and resource settings.

Templates should not contain scientific logic. They should call scripts from `scripts/` and load site configuration from `configs/sites/`.
