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

# Calculate the 0-based index for the interval file
INDEX=$SLURM_ARRAY_TASK_ID
INTERVAL_FILE=$(printf "%04d-scattered.interval_list" $INDEX)

TMP_DIR=/scratch/users/$USER/tmp/$SLURM_JOBID

mkdir -p $TMP_DIR

# gatk command and arguments
gatk --java-options "-Djava.io.tmpdir=$TMP_DIR -Xms${MEM}G -Xmx${MEM}G -XX:ParallelGCThreads=${CPUS}" HaplotypeCaller \
    -R ${REFERENCE} \
    -I ${INPUT_BAM} \
    -O ${OUTPUT_DIR}/output_${SAMPLEID}_${INDEX}.g.vcf.gz \
    -ip 100 \
    --intervals "${INTERVALS_DIR}/${INTERVAL_FILE}" \
    --emit-ref-confidence GVCF \
    --output-mode EMIT_ALL_CONFIDENT_SITES \
    --dbsnp $DBSNP \
    --native-pair-hmm-threads 2

wait 1

rm -rf $TMP_DIR

END_TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
echo "Job ended at: $END_TIMESTAMP"