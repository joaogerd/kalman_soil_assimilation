#!/usr/bin/env bash
# Runtime defaults for JACI-like PBS environments.
# Review all values on the target machine before operational use.

export KSA_SITE_NAME="jaci"
export KSA_PBS_QUEUE="workq"
export KSA_PBS_ACCOUNT="CHANGE_ME"
export KSA_WALLTIME="00:30:00"
export KSA_NODES="1"
export KSA_NCPUS="1"
export KSA_MEM="4gb"
export KSA_OMP_NUM_THREADS="1"
