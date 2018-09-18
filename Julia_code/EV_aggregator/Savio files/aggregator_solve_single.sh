#!/bin/bash
# Job name:
#SBATCH --job-name=aggregator
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
#SBATCH --time=10:00:30
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

module load julia
julia aggregator_single.jl $1 $SLURM_JOB_ID; 
env