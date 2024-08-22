#!/bin/bash
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=01:00:00
#SBATCH --partition=short

# Activate conda environment
source ~/.bashrc
conda activate genomics_pipeline

# Get the current date and time
START_TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
echo "Job started at: $START_TIMESTAMP"
echo "Job started at: $START_TIMESTAMP"
echo "Job started at: $START_TIMESTAMP"
echo "Job Name: ${SLURM_JOB_NAME}"
echo "Job ID: ${SLURM_JOB_ID}"
echo "Partition: ${SLURM_JOB_PARTITION}"
echo "Nodes: ${SLURM_JOB_NUM_NODES}"
echo "CPUs per Task: ${SLURM_CPUS_PER_TASK}"
echo "Memory: ${SLURM_MEM_PER_NODE}"
echo "Time Limit: ${SLURM_TIMELIMIT}"

module load multiqc

# Run MultiQC
multiqc ${INPUT_DIR} -o ${OUTPUT_DIR}/${SAMPLEID}.multiqc_report

END_TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
echo "Job ended at: $END_TIMESTAMP"
