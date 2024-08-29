import os 
import yaml
import glob

def mkdir(directory):
  os.makedirs(directory, exist_ok=True)
  return
  
def load_config(config_path):
  with open(config_path, 'r') as file:
    return yaml.safe_load(file)
    
def get_resources(config, module_name):
  try:
    resources = config['modules_resources']['module'][module_name]
    cpus = resources['cpus']
    mem = resources['mem']
    return cpus, mem
  except KeyError as e:
    raise ValueError(f"Module '{module_name}' not found in the config file.") from e

    
def erase_data(sampleid, outputdir):
  """Delete intermediate BAM and BAI files."""
  patterns_to_delete = [
      f"{outputdir}/**/{sampleid}.sorted.bam",
      f"{outputdir}/**/{sampleid}.sorted.bam.bai",
      f"{outputdir}/**/{sampleid}.fixed.bam",
      f"{outputdir}/**/{sampleid}.fixed.bam.bai",
      f"{outputdir}/**/{sampleid}.filtered.bam",
      f"{outputdir}/**/{sampleid}.filtered.bam.bai"
  ]

  for pattern in patterns_to_delete:
    files_to_delete = glob.glob(pattern, recursive=True)
    for file in files_to_delete:
      try:
        os.remove(file)
        print(f"Deleted: {file}")
      except OSError as e:
        print(f"Error deleting file {file}: {e}")
  return     

    
