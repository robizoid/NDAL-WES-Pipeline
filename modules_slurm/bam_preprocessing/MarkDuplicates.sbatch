#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=01:00:00
#SBATCH --partition=short

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

TMP_DIR=/scratch/users/$USER/tmp/$SLURM_JOBID
mkdir -p $TMP_DIR

module load gatk

OUTPUT_BAM="${OUTPUT_DIR}/${SAMPLEID}.rmdup.bam"
METRICS_FILE="${OUTPUT_DIR}/${SAMPLEID}.rmdup.metrics.txt"

gatk --java-options "-Djava.io.tmpdir=$TMP_DIR -Xms${MEM}G -Xmx${MEM}G -XX:+UseParallelGC -XX:ParallelGCThreads=${CPUS}" MarkDuplicates \
  -I ${INPUT_BAM} \
  -O ${OUTPUT_BAM} \
  -M ${METRICS_FILE} \
  --CREATE_INDEX

sleep 1

rm -rf $TMP_DIR

END_TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
echo "Job ended at: $END_TIMESTAMP"