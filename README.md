# NDAL-KUTTAM-HPC - Whole Exome Sequencing Pipeline - Raw Data to gVCF

## Preambule
The pipeline is mainly dedicated to process WES data of NDAL team on the HPC of Koç University.
It uses the job scheduler SLURM to stage all jobs to process raw data and generate all files.

![image](https://github.com/user-attachments/assets/250ea682-1fe6-4869-aa6d-aa81c9de53a1)


## Installation

To set up the conda environment for the pipeline, follow these steps:

1. Clone the repository:

   To get started, clone the repository:
   ```bash
   git clone https://github.com/robizoid/NDAL-WES-Pipeline.git
   cd NDAL-WES-Pipeline

2. Create `conda` environment:
   
   Create the `conda` environment using the provided environment.yml file:
   ```bash
   conda env create -f environment.yml
3. Activate environment:
	Activate the newly created `genomics_pipeline` environment
   ```bash
   conda activate genomics_pipeline
5. Test environment:
	Run the following command to ensure the installation was successful, it should return similar output:
   ```bash
   python main.py --help
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

To run the pipeline on one WES sample, use the following command:

    python main.py --config /path/to/config.yaml --output /path/to/output/dir --assembly GRCh38 --read1 /path/to/sample_R1.fastq.gz --read2 /path/to/sample_R2.fastq.gz --sample SAMPLEID --targets sureselectv6

The command will stage all slurm modules that will process the raw and generate:

 - Intermediary BAM files 
 - GVCF file 
 - Quality Metric

### Run as a batch

To process a Sequencing batch, you can use the `run_cohort.py`.
#### Recommended Practice
It is always safe to run `tmux`, a terminal multiplexer, that lets you switch easily between several programs in one terminal. 
In other word, it creates sub-terminal where you can run scripts that won't get interrupted when you leave the terminal or disconnect from HPC.

You can create a tmux terminal as followed:

    tmux new-session -s <name>
    
It will create the tmux window with the given name you chose.

Then, you need to create a metadata table as followed:

    python generate_samples_spreadsheet.py --input_dir <sequencing_batch_folder> --output_tsv <OUTPUT.tsv> --assembly GRCh38 --targets <exome_kit>

Then,

    python run_cohort.py --tsv <OUTPUT.tsv> --config config.yaml

Since, it is a `python` script running you do not want to interrupt it... unless you really want (<kbd>ctrl</kbd> + <kbd>c</kbd>).
Otherwise you can detach the tmux window and get back to your initial terminal by doing the following command combination:
<kbd>ctrl</kbd> + <kbd>b</kbd> + <kbd>d</kbd>

If you want to go back to the terminus window, run the following command:

    tmux a -t <name>

