#!/usr/bin/env bash
# Runtime defaults for JACI PBS environments.
# Values are based on the queue list observed on JACI and should be reviewed before operational use.

export KSA_SITE_NAME="jaci"
export KSA_PBS_QUEUE="pesqmini"
export KSA_PBS_ACCOUNT="CHANGE_ME"
export KSA_WALLTIME="00:30:00"
export KSA_NODES="1"
export KSA_NCPUS="1"
export KSA_MEM="4gb"
export KSA_OMP_NUM_THREADS="1"

# Observed enabled queues include: aux, pesqextra, pesqhigh, pesqmidi, pesqmini, oper, preoper and longtime.
# The queue workq was observed as disabled and should not be used as the default.
