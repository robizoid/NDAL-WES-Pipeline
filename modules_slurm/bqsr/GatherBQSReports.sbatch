#!/bin/bash
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4gb
#SBATCH --time=01:00:00
#SBATCH --partition=mid


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

module load gatk

OUTPUT_FILE="${BQSR_DIR}/gathered_recal_data.table"

# Generate the list of input files dynamically
# Define the maximum index to gather up to
MAX_INDEX=${ARRAY_INDICES}
INPUT_FILES=""
for i in $(seq 0 $MAX_INDEX); do
    INPUT_FILES+="-I ${BQSR_DIR}/recal_data_${i}.table "
done


gatk GatherBQSRReports $INPUT_FILES -O $OUTPUT_FILE

END_TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
echo "Job ended at: $END_TIMESTAMP"