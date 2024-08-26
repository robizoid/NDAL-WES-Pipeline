#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=02:00:00
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
module load samtools

TMP_DIR=/scratch/users/$USER/tmp/$SLURM_JOBID
mkdir -p $TMP_DIR

OUTPUT_BAM="${OUTPUT_DIR}/${SAMPLEID}.recalibrated.bam"

# ApplyBQSR
gatk --java-options "-Djava.io.tmpdir=$TMP_DIR -Xms${MEM}G -Xmx${MEM}G -XX:ParallelGCThreads=${CPUS}" ApplyBQSR \
    -R ${REFERENCE} \
    -I ${INPUT_BAM} \
    --bqsr-recal-file ${BQSR_TABLE} \
    --create-output-bam-index true \
    -O ${OUTPUT_BAM}

sleep 1

rm -rf $TMP_DIR



END_TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
echo "Job ended at: $END_TIMESTAMP"
