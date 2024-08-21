#!/bin/bash
#SBATCH --nodes=1
#SBATCH --cpus-per-task=2
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

# Calculate the 0-based index for the interval file
INDEX=$SLURM_ARRAY_TASK_ID
INTERVAL_FILE=$(printf "%04d-scattered.interval_list" $INDEX)

TMP_DIR=/scratch/users/$USER/tmp/$SLURM_JOBID

mkdir -p $TMP_DIR

echo $INDEX

# BaseRecalibrator
gatk --java-options "-Djava.io.tmpdir=$TMP_DIR -Xms4G -Xmx4G -XX:ParallelGCThreads=2" BaseRecalibrator \
    -R $REFERENCE \
    -I $INPUT_BAM \
    --known-sites $DBSNP \
    --known-sites $MILLS_INDELS \
    -L "${INTERVALS_DIR}/${INTERVAL_FILE}" \
    -O "${OUTPUT_DIR}/recal_data_${INDEX}.table"

rm -rf $TMP_DIR


END_TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
echo "Job ended at: $END_TIMESTAMP"