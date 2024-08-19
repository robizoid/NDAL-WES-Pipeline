import subprocess
import logging
import os
import datetime

def run_command(command, output_dir, log_prefix="General"):
    """Run a shell command and log outputs to a file with a specific prefix in the specified output directory."""

    # Ensure the output directory for logs exists
    log_directory = os.path.join(output_dir, "logs")
    os.makedirs(log_directory, exist_ok=True)
    
    # Create a unique log file for each run
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"{log_prefix}_{timestamp}.log"
    log_path = os.path.join(log_directory, log_filename)

    # Configure logging
    logger = logging.getLogger(log_prefix)
    logger.setLevel(logging.DEBUG)
    # Remove all handlers associated with the logger object by default
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Execute and log the command
    logger.info(f"Executing command: {command}")
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
        logger.debug(f"Command output: {output}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running command: {e.cmd}")
        logger.error(f"Command output: {e.output}")
        raise
    finally:
        # Remove file handler after command execution to prevent memory leaks
        logger.removeHandler(file_handler)
    
    return output

def submit_job(script_path, job_name, output_dir, log_prefix="Undefined", array_range=None, dependency=None):
    """
    Submits a job to SLURM using sbatch.

    Parameters:
    - script_path (str): Path to the SLURM batch script to be executed.
    - job_name (str): Name of the job.
    - array_range (str): Range for array jobs (e.g., "1-10"). Default is None.
    - dependency (str): Job dependency in the format "afterok:<job_id>". Default is None.

    Returns:
    - job_id (str): The job ID assigned by SLURM.
    """
    command = ['sbatch', '--job-name', job_name]

    if array_range:
        command.extend(['--array', array_range])
    
    if dependency:
        command.extend(['--dependency', dependency])

    command.append(script_path)

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        # Extract the job ID from the output
        output = result.stdout
        job_id = output.split()[-1]  # Assuming the job ID is the last word in the output
        return job_id
    except subprocess.CalledProcessError as e:
        print(f"Error submitting job: {e.stderr}")
        return None
