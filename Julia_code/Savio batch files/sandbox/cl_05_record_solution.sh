#!/bin/bash
# Job name:
#SBATCH --job-name=db_write
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
#SBATCH --ntasks-per-node=1
#
# Number of processors for single task needed for use case (example):
#SBATCH --cpus-per-task=1
#
# Mail type:
#SBATCH --mail-type=all
#
# Mail user:
#SBATCH --mail-user=jdlara@berkeley.edu
#
# Wall clock limit:
#SBATCH --time=01:00:00
#
# first job - generate data files
module load matlab
matlab -nosplash -nodisplay < cl_05_record_solution.m 
env
