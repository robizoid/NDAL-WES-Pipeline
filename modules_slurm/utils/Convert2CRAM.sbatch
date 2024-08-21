#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=02:00:00
#SBATCH --partition=short
#SBATCH --cpus-per-task=20

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

OUTPUT_CRAM="${OUTPUT_DIR}/${SAMPLEID}.${BAM_TYPE}.cram"

TMP_DIR=/scratch/users/$USER/tmp/$SLURM_JOBID
mkdir -p $TMP_DIR

module load samtools

samtools view -@20 -C -T ${REFERENCE} -o ${OUTPUT_CRAM} ${INPUT_BAM}

wait 1

rm -rf $TMP_DIR

END_TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
echo "Job ended at: $END_TIMESTAMP"