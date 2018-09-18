#!/bin/bash
# Job name:
#SBATCH --job-name=init_z_problem
#
# Account:
#SBATCH --account=fc_emac
#
# QoS:
#SBATCH --qos=savio_normal
#
# Partition:
#SBATCH --partition=savio
#
# Wall clock limit:
#SBATCH --time=00:50:30
#
# Processors:
#SBATCH --nodes=1
#SBATCH --exclusive
#
# Mail type:
# --mail-type=all
#
# Mail user:
# --mail-user=jdlara@berkeley.edu
#
## Run the initialization of the z_problem
module load matlab
matlab -nosplash -nodisplay < cl_04_solve_z_model.m 
env
