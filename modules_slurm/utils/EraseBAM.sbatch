#!/bin/bash
#SBATCH --partition=short
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=01:00:00

# Get the current date and time
START_TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
echo "Job started at: $START_TIMESTAMP"
echo "Job Name: ${SLURM_JOB_NAME}"
echo "Job ID: ${SLURM_JOB_ID}"
echo "Partition: ${SLURM_JOB_PARTITION}"
echo "Nodes: ${SLURM_JOB_NUM_NODES}"
echo "CPUs per Task: ${SLURM_CPUS_PER_TASK}"
echo "Memory: ${SLURM_MEM_PER_NODE}"
echo "Time Limit: ${SLURM_TIMELIMIT}"

# Define the patterns to delete
patterns_to_delete=(
    "${OUTPUT_DIR}/**/${SAMPLEID}.sorted.bam"
    "${OUTPUT_DIR}/**/${SAMPLEID}.sorted.bam.bai"
    "${OUTPUT_DIR}/**/${SAMPLEID}.fixed.bam"
    "${OUTPUT_DIR}/**/${SAMPLEID}.fixed.bam.bai"
    "${OUTPUT_DIR}/**/${SAMPLEID}.filtered.bam"
    "${OUTPUT_DIR}/**/${SAMPLEID}.filtered.bam.bai"
    "${OUTPUT_DIR}/**/${SAMPLEID}.recalibrated.bam"
    "${OUTPUT_DIR}/**/${SAMPLEID}.recalibrated.bai"
    "${OUTPUT_DIR}/**/${SAMPLEID}.rmdup.bam"
    "${OUTPUT_DIR}/**/${SAMPLEID}.rmdup.bam.bai"
)

# Loop over each pattern and delete the matching files
for pattern in "${patterns_to_delete[@]}"; do
    # Use find to locate files recursively and delete them
    find $pattern -type f -exec rm -v {} \;
done