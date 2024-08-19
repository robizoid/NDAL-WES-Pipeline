#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=02:00:00
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

TMP_DIR=/scratch/users/$USER/$SLURM_JOBID
mkdir -p $TMP_DIR

module load gatk
module load samtools

OUT_BAM_FILE="${OUTPUT_DIR}/${SAMPLEID}.fixed.bam"

gatk --java-options "-Djava.io.tmpdir=$TMP_DIR -Xmx${MEM}G -XX:+UseParallelGC -XX:ParallelGCThreads=${CPUS}" FixMateInformation \
    --MAX_RECORDS_IN_RAM 2000000 \
    --VALIDATION_STRINGENCY SILENT \
    --ASSUME_SORTED true \
    --CREATE_INDEX true \
    -I ${INPUT_BAM} \
    -O ${OUT_BAM_FILE}
    
wait 1

rm -rf $TMP_DIR

END_TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
echo "Job ended at: $END_TIMESTAMP"