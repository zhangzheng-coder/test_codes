#!/bin/bash
# Job name:
#SBATCH --job-name=x_problem
#
# Account:
#SBATCH --account=fc_emac
#
# QoS:
#SBATCH --qos=savio_normal
#
# Partition:
#SBATCH --partition=savio2
#
# Wall clock limit:
#SBATCH --time=02:00:00
#
# Request one node:
#SBATCH --nodes=1
#
# Specify number of tasks for use case (example):
# --ntasks-per-node=20
#
# Mail type:
# --mail-type=all
#
# Mail user:
#SBATCH --mail-user=jdlara@berkeley.edu

module load matlab
matlab -nosplash -nodisplay -r "cl_03_solve_x_model(${SLURM_ARRAY_TASK_ID})"
env
