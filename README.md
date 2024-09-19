# NDAL-KUTTAM-HPC - Whole Exome Sequencing Pipeline - Raw Data to gVCF

## Preambule
The pipeline is mainly dedicated to process WES data of NDAL team on the HPC of Koç University.
It uses the job scheduler SLURM to stage all jobs to process raw data and generate all files.

## Installation 

### Setup Conda Environment

To set up the conda environment for the pipeline, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/robizoid/NDAL-WES-Pipeline.git
   cd NDAL-WES-Pipeline

2. Create `conda` environment :
  ```bash
  conda env create -f environment.yml

3. Activate `conda` environment:
  ```bash
  conda activate genomics_pipeline

4. Test installation:
```bash
python main.py --help

Should return
```bash
usage: main.py [-h] --config CONFIG --output OUTPUT --assembly ASSEMBLY --read1 READ1 --read2 READ2 --sample SAMPLE --targets TARGETS

Run the genomic pipeline.

optional arguments:
  -h, --help           show this help message and exit
  --config CONFIG      Path to the configuration file
  --output OUTPUT      Path to the output directory
  --assembly ASSEMBLY  Assembly version [GRCh38]
  --read1 READ1        Path to read 1 fastq file
  --read2 READ2        Path to read 2 fastq file
  --sample SAMPLE      Sample ID
  --targets TARGETS    Exome Kits [sureselectv6, nextera]

## Usage
