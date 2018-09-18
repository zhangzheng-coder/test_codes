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
# Request one node:
#SBATCH --nodes=1
#
# Specify one task:
#SBATCH --nodes=1
#SBATCH --exclusive
#
# Mail type:
#SBATCH --mail-type=all
#
# Mail user:
#SBATCH --mail-user=jdlara@berkeley.edu
#
# Wall clock limit:
#SBATCH --time=05:00:00
#

module load julia

julia aggregator_single.jl Price_profiles/CA_Weighted_Price_Case0.csv $SLURM_JOB_ID

env
