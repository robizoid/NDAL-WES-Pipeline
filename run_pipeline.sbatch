#!/bin/bash
#SBATCH --job-name=cohort_genomics_pipeline_job
#SBATCH --partition=mid
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=32G
#SBATCH --time=3:00:00
#SBATCH --output=cohort_genomics_pipeline_job.out
#SBATCH --error=cohort_genomics_pipeline_job.err

# Activate conda environment
source ~/.bashrc
conda activate genomics_pipeline

# path to main script
PIPELINE_SCRIPT="/scratch/users/rpalvadeau/hpc_run/ndal/genomics/pipeline/wes/main_new.py"

# config file to import
CONFIG_FILE="/scratch/users/rpalvadeau/hpc_run/ndal/genomics/pipeline/wes/config.yaml"

tail -n +2 "$TSV_FILE" | while IFS=$'\t' read -r SAMPLEID READ1 READ2 OUTPUTDIR ASSEMBLY TARGETS
do
    echo "Starting pipeline for sample: $SAMPLEID"

    # Run the pipeline script for each sample
    # python $PIPELINE_SCRIPT --config $CONFIG_FILE --output $OUTPUTDIR --assembly $ASSEMBLY --read1 $READ1 --read2 $READ2 --sample $SAMPLEID --targets $TARGETS

    echo "Pipeline finished for sample: $SAMPLEID"
    #echo "--------------------------------------"

done