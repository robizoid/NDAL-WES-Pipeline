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


module load bwa
module load samtools

# Activate conda environment
source ~/.bashrc
conda activate genomics_pipeline

TMP_DIR=/scratch/users/$USER/tmp/$SLURM_JOBID
mkdir -p $TMP_DIR

OUT_BAM_FILE="${OUTPUT_DIR}/${SAMPLEID}.sorted.bam"

fastp -i ${READ1} -I ${READ2} --stdout --thread 2 -j "${OUTPUT_DIR}/fastp-${SLURM_JOBID}.${SAMPLEID}.json" -h "${OUTPUT_DIR}/fastp-${SLURM_JOBID}.${SAMPLEID}.html" 2> "${OUTPUT_DIR}/fastp-${SLURM_JOBID}.${SAMPLEID}.log" | bwa mem -M -v 2 -p -t 20 -R "@RG\\tID:${SAMPLEID}\\tSM:${SAMPLEID}\\tPL:ILLUMINA\\tLB:${SAMPLEID}" ${REFERENCE} - | samtools sort -m 1706M --threads 10 -T $TMP_DIR -o ${OUT_BAM_FILE}

samtools index -@ 16 ${OUT_BAM_FILE}

sleep 1

rm -rf $TMP_DIR

END_TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
echo "Job ended at: $END_TIMESTAMP"