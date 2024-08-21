import subprocess
import os
import logging

def submit_job(sbatch_script, export, output_dir, job_name, dependency=None, array=None, cpus=None, mem=None):
    # Construct the log file paths
    output_log = os.path.join(output_dir, f"{job_name}_%j.out")
    error_log = os.path.join(output_dir, f"{job_name}_%j.err")
    
    # Construct the sbatch command
    command = f"sbatch --export={export} --output={output_log} --error={error_log}"
    if dependency:
        command += f" --dependency=afterok:{dependency}"
    if array:
        command += f" --array={array}"
    if cpus:
        command += f" --cpus-per-task={cpus}"
    if mem:
        command += f" --mem={mem}G"    
    command += f" {sbatch_script}"
    
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).strip().decode()
        logging.info(f"sbatch output: {output}")
        job_id = output.split()[-1]
        return job_id
    except subprocess.CalledProcessError as e:
        logging.error(f"Error submitting job: {e.output.decode()}")
        return None
    except IndexError as e:
        logging.error(f"Error parsing job ID from sbatch output: {output}")
        return None