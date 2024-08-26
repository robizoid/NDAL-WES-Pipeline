#!/bin/bash
#SBATCH --job-name=mosdepth
#SBATCH --nodes=1
#SBATCH --time=01:00:00
#SBATCH --partition=short

# Activate conda environment
source ~/.bashrc
conda activate genomics_pipeline

# Get the current date and time
START_TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
echo "Job started at: $START_TIMESTAMP"
echo "Job started at: $START_TIMESTAMP"
echo "Job Name: ${SLURM_JOB_NAME}"
echo "Job ID: ${SLURM_JOB_ID}"
echo "Partition: ${SLURM_JOB_PARTITION}"
echo "Nodes: ${SLURM_JOB_NUM_NODES}"
echo "CPUs per Task: ${SLURM_CPUS_PER_TASK}"
echo "Memory: ${SLURM_MEM_PER_NODE}"
echo "Time Limit: ${SLURM_TIMELIMIT}"


RECALIBRATED_BAM_DIR="${INPUT_FOLDER}/bqsr"
RMDUP_BAM_DIR="${INPUT_FOLDER}"

# List of BAM types and their corresponding directories
declare -A BAM_PATHS
BAM_PATHS["recalibrated"]="${RECALIBRATED_BAM_DIR}/${SAMPLEID}.recalibrated.bam"
BAM_PATHS["filtered"]="${RMDUP_BAM_DIR}/${SAMPLEID}.filtered.bam"
BAM_PATHS["fixed"]="${RMDUP_BAM_DIR}/${SAMPLEID}.fixed.bam"
BAM_PATHS["rmdup"]="${RMDUP_BAM_DIR}/${SAMPLEID}.rmdup.bam"

for BAM_TYPE in "${!BAM_PATHS[@]}"; do
    INPUT_BAM="${BAM_PATHS[$BAM_TYPE]}"
    OUTPUT_PREFIX="${OUTPUT_DIR}/${SAMPLEID}.${BAM_TYPE}"

    if [ -f "$INPUT_BAM" ]; then
        echo "Processing $INPUT_BAM"

        mosdepth --threads ${CPUS} --by ${TARGETS} ${OUTPUT_PREFIX} ${INPUT_BAM}

        echo "Finished processing $INPUT_BAM"
    else
        echo "File $INPUT_BAM does not exist, skipping."
    fi
done

sleep 1

END_TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
echo "Job ended at: $END_TIMESTAMP"
