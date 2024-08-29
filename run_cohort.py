import os
import sys
import time
import subprocess
import argparse
import pandas as pd
from main import main  

def wait_for_job_completion(job_id):
    """Wait for the SLURM job with job_id to complete."""
    while True:
        result = subprocess.run(
            ["squeue", "--job", job_id],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        if job_id not in result.stdout.decode():
            break
        
        sys.stdout.write(f"\rWaiting for job {job_id} to complete...")
        sys.stdout.flush()
        time.sleep(60)  # Check every minute
    sys.stdout.write("\rJob completed.                          \n")
    sys.stdout.flush()

def run_pipeline_for_cohort(tsv_file, config):
    # Read the TSV file
    samples = pd.read_csv(tsv_file, sep='\t')
    
    last_job_id = None

    for index, row in samples.iterrows():
        sampleid = row['SAMPLEID']
        read1 = row['READ1']
        read2 = row['READ2']
        output_dir = row['OUTPUTDIR']
        assembly = row['ASSEMBLY']
        targets = row['TARGETS']
        
        print(f"Pipeline started for sample: {sampleid}")
        
        # Construct arguments for the main function
        args = argparse.Namespace(
            config=config,
            output=output_dir,
            assembly=assembly,
            read1=read1,
            read2=read2,
            sample=sampleid,
            targets=targets
        )

        # Run the pipeline
        last_job_id = main(args)

        # Wait for the last job to finish before proceeding
        if last_job_id:
            wait_for_job_completion(last_job_id)

        print(f"Pipeline finished for sample: {sampleid}")
        print("--------------------------------------")
    
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the cohort genomics pipeline.")
    parser.add_argument("--tsv", required=True, help="Path to the TSV file with sample information")
    parser.add_argument("--config", required=True, help="Path to the configuration file")

    args = parser.parse_args()
    run_pipeline_for_cohort(args.tsv, args.config)
