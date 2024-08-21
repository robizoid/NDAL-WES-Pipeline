#!/bin/bash

# Define directories
FASTQ_DIR="/path/to/fastq"
BAM_DIR="/path/to/bam"
BQSR_DIR="/path/to/bqsr"
OUTPUT_DIR="/path/to/output"
LOG_DIR="/path/to/logs"
INTERVALS_DIR="/path/to/intervals"
REFERENCE="/kuttam_fg/refdata/robin/references/Homo_sapiens/GATK/GRCh38/Sequence/WholeGenomeFasta/Homo_sapiens_assembly38.fasta"
KNOWN_SITES=(
    "/kuttam_fg/refdata/robin/references/Homo_sapiens/GATK/GRCh38/Annotation/GATKBundle/dbsnp_146.hg38.vcf.gz"
    "/kuttam_fg/refdata/robin/references/Homo_sapiens/GATK/GRCh38/Annotation/GATKBundle/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz"
)

# Define SLURM parameters
SBATCH_OPTIONS="--partition=mid --time=02:00:00 --mem=8gb --cpus-per-task=2"

