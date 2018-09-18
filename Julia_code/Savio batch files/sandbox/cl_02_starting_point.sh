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
#SBATCH --time=02:00:00
#
# Processors:
#SBATCH --nodes=1
#SBATCH --exclusive
#
# Mail type:
#SBATCH --mail-type=all
#
# Mail user:
#SBATCH --mail-user=jdlara@berkeley.edu
#
## Run the initialization of the z_problem
module load matlab
matlab -nosplash -nodisplay < cl_02_starting_point.m 
env
