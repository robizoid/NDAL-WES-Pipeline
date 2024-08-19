#!/bin/bash
#SBATCH --job-name=QC-fastqc
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=6gb
#SBATCH --time=01:00:00
#SBATCH --partition=short

# Get the current date and time
START_TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
echo "Job Name: ${SLURM_JOB_NAME}"
echo "Job ID: ${SLURM_JOB_ID}"
echo "Partition: ${SLURM_JOB_PARTITION}"
echo "Nodes: ${SLURM_JOB_NUM_NODES}"
echo "CPUs per Task: ${SLURM_CPUS_PER_TASK}"
echo "Memory: ${SLURM_MEM_PER_NODE}"
echo "Time Limit: ${SLURM_TIMELIMIT}"

echo "Job started at: $START_TIMESTAMP"

module load fastqc

fastqc ${READ1} ${READ2} -o ${OUTPUT_DIR} --noextract

END_TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
echo "Job ended at: $END_TIMESTAMP"
