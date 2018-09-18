#!/bin/bash
# Job name:
#SBATCH --job-name=dr_project_main
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
#SBATCH --mail-user=fcastro@berkeley.edu
# Wall clock limit:
#SBATCH --time=00:50:30
#
#create a folder to store the intermediate files according to the number of the main 
#slurm ID. 

#mkdir -p $SLURM_JOB_ID

# first job - Datafiles
data_prep=$(sbatch cl_01_data_processing.sh | awk '{print $NF}')
sleep 60 

# Definition of the loop control variables 
array_size=$(head -1 TEMP/n.par)
declare -i iteration_size=$(head -1 TEMP/iter.par)
z_end="z$iteration_size"

# second job - initialization of the z problem. The number of the problem Z1 is hardcoded
# on purpose

z1=$(sbatch --dependency=afterok:$data_prep cl_02_starting_point.sh | awk '{print $NF}')

for ((n=2;n <=  $iteration_size;n++))  
	do 

count=`expr $n - 1`


# X problems are defined as an array of multiple jobs dependent on a single job, in this
# corresponds to the z problem.

z_count="z$count"
eval "x$count=$(sbatch --array=1-$array_size --dependency=afterok:${!z_count} cl_03_solve_x_model.sh | awk '{print $NF}')"
sleep 1

#The iterative process of the ADMM algorithm starts here, after the solution of the array
# of X problems, the following z model solution task is created

x_count="x$count"
eval "z$n=$(sbatch --dependency=afterok:${!x_count} cl_04_solve_z_model.sh | awk '{print $NF}')"
sleep 1

done

record_solution=$(sbatch --dependency=afterok:${!z_end} cl_05_record_solution.sh | awk '{print $NF}')

env
