import subprocess
import time
import yaml
import argparse
import logging
import os
from utils.submit_job import submit_job
from utils.logg_utils import setup_logging, log_message
from utils.utils import mkdir, load_config, erase_data, get_resources


def main(args):
  # Set up logging
  main_output_dir = args.output
  # Set Main directory path
  script_dir = os.path.dirname(os.path.realpath(__file__))
  # Create output directory if it doesn't exist
  mkdir(main_output_dir)
  pipeline_log = os.path.join(main_output_dir, 'pipeline.log')
  logging.basicConfig(filename=pipeline_log, level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
  log_message("Starting pipeline")

  # Pipeline
  try:
    config = load_config(args.config)
    assembly = args.assembly
    read1 = args.read1 
    read2 = args.read2
    sampleid = args.sample
    targets = args.targets
    
    if args.assembly == "GRCh37":
      reference = config['reference_genome']["grch37"]
      kit = config['exomes_kits']['grch37'][targets]
    else:
      reference = config['reference_genome']["grch38"]
      kit = config['exomes_kits']['grch38'][targets]
      
    dbsnp = config['gatk_ressources']['known_sites']['dbsnp']
    mills_indels = config['gatk_ressources']['known_sites']['mills_indels']

    # Step 1: QC - FastQC
    log_message("Initiating FastQC - Job Submission")
    output_dir = os.path.join(main_output_dir, "qc")
    mkdir(output_dir)
    fastqc_module = os.path.join(script_dir, "modules_slurm/qc/fastqc.sbatch")
    fastqc_job = submit_job(
            fastqc_module,
            export=f"READ1={read1},READ2={read2},OUTPUT_DIR={output_dir}",
            output_dir=output_dir,
            job_name="QC-FASTQC"
        )
    if fastqc_job:
      log_message(f"FastQC job submitted with ID: {fastqc_job}")
    else:
      log_message("FastQC job submission failed")

    # Step 2: Alignment - BWA
    log_message("Initiating Alignment BWA - Job Submission")
    output_dir = os.path.join(main_output_dir, "alignment")
    mkdir(output_dir)
    alignment_module = os.path.join(script_dir, "modules_slurm/alignment/bwa.sbatch")
    cpus, mem = get_resources(config, "alignment")
    bwa_job = submit_job(
            alignment_module,
            export=f"READ1={read1},READ2={read2},REFERENCE={reference},SAMPLEID={sampleid},OUTPUT_DIR={output_dir},MEM={mem},CPUS={cpus}",
            output_dir=output_dir,
            job_name="ALIGNMENT-FASTP-BWA-SAMTOOLS",
            cpus=cpus,
            mem=mem
        )
    sorted_bam = os.path.join(output_dir, f"{sampleid}.sorted.bam")
    if bwa_job:
      log_message(f"BWA job submitted with ID: {bwa_job}")
    else:
      log_message("BWA job submission failed")

    
    # Step 3: Bam Preprocessing - GATK - FixMateInformation
    log_message("Initiating FixMateInformation GATK - Job Submission")
    output_dir = os.path.join(main_output_dir, "bam_preprocessing")
    mkdir(output_dir)
    fix_mate_module = os.path.join(script_dir, "modules_slurm/bam_preprocessing/FixMateInformation.sbatch")
    cpus, mem = get_resources(config, "fixmate")
    fix_mate_job = submit_job(
            fix_mate_module,
            export=f"INPUT_BAM={sorted_bam},SAMPLEID={sampleid},OUTPUT_DIR={output_dir},CPUS={cpus},MEM={mem}",
            output_dir=output_dir,
            job_name="BAM-Preprocessing-GATK-FixMateInformation",
            dependency=bwa_job,
            cpus=cpus,
            mem=mem
        )
    fixed_bam = os.path.join(output_dir, f"{sampleid}.fixed.bam")
    if fix_mate_job:
      log_message(f"GATK-FixMateInformation job submitted with ID: {fix_mate_job}")
    else:
      log_message("GATK-FixMateInformation job submission failed")
      
    # Step 4: Bam Preprocessing - GATK - MarkDuplicates
    log_message("Initiating MarkDuplicates GATK - Job Submission")
    output_dir = os.path.join(main_output_dir, "bam_preprocessing")
    mkdir(output_dir)
    mark_duplicates_module = os.path.join(script_dir, "modules_slurm/bam_preprocessing/MarkDuplicates.sbatch")
    cpus, mem = get_resources(config, "markduplicates")
    rmdup_job = submit_job(
            mark_duplicates_module,
            export=f"INPUT_BAM={fixed_bam},SAMPLEID={sampleid},OUTPUT_DIR={output_dir},MEM={cpus},CPUS={cpus}",
            output_dir=output_dir,
            job_name="BAM-Preprocessing-GATK-MarkDuplicates",
            dependency=fix_mate_job,
            cpus=cpus,
            mem=mem
        )
    rmdup_bam = os.path.join(output_dir, f"{sampleid}.rmdup.bam")
    if rmdup_job:
      log_message(f"GATK-MarkDuplicates job submitted with ID: {rmdup_job}")
    else:
      log_message("GATK-MarkDuplicates job submission failed")
    
    # Step 5: BQSR - GATK - SplitIntervals
    log_message("Initiating BQSR GATK - Split Intervals - Job Submission")
    output_dir = os.path.join(main_output_dir, "bam_preprocessing/bqsr")
    mkdir(output_dir)
    split_int_bqsr_module = os.path.join(script_dir, "modules_slurm/bqsr/ScatterIntervals.sbatch")
    nb_split = 24
    bqsr_split_intervals_job = submit_job(
            split_int_bqsr_module,
            export=f"INPUT_BAM={rmdup_bam},SAMPLEID={sampleid},REFERENCE={reference},OUTPUT_DIR={output_dir},NB_SPLIT={nb_split}",
            output_dir=output_dir,
            job_name="GATK-Split-Intervals",
            dependency=rmdup_job,
            cpus=cpus,
            mem=mem
        )
    intervals_dir = os.path.join(output_dir, f"intervals")
    if bqsr_split_intervals_job:
      log_message(f"GATK - Split Intervals job submitted with ID: {bqsr_split_intervals_job}")
    else:
      log_message("GATK - Split Intervals job submission failed")
      
    # Step 6: BQSR - GATK - BQSR intervals
    log_message("Initiating BQSR GATK - Generate Split Tables - Job Submission")
    bqsr_int_module = os.path.join(script_dir, "modules_slurm/bqsr/IntervalsBQSR.sbatch")
    cpus, mem = get_resources(config, "intervalsBQSR")
    bqsr_intervals_job = submit_job(
        bqsr_int_module,
        export=f"INPUT_BAM={rmdup_bam},SAMPLEID={sampleid},REFERENCE={reference},DBSNP={dbsnp},MILLS_INDELS={mills_indels},OUTPUT_DIR={output_dir},INTERVALS_DIR={intervals_dir},MEM={mem},CPUS={cpus}",
        output_dir=output_dir,
        job_name="GATK-BQSR-Intervals",
        dependency=bqsr_split_intervals_job,
        array="0-23",
        cpus=cpus,
        mem=mem
    )
    if bqsr_intervals_job:
      log_message(f"BQSR GATK job submitted with ID: {bqsr_intervals_job}")
    else:
      log_message("BQSR GATK Filtration job submission failed")
      
    # Step 7: BQSR - GATK - Gather Reports
    log_message("Initiating BQSR GATK - Gather Reports - Job Submission")
    gather_reports_bqsr_module = os.path.join(script_dir, "modules_slurm/bqsr/GatherBQSReports.sbatch")
    bqsr_gather_reports_job = submit_job(
            gather_reports_bqsr_module,
            export=f"BQSR_DIR={output_dir},ARRAY_INDICES=23",
            output_dir=output_dir,
            job_name="GATK-BQSR-GatherReports",
            dependency=bqsr_intervals_job
        )
    gathered_report = os.path.join(output_dir, f"gathered_recal_data.table")
    if bqsr_gather_reports_job:
      log_message(f"BQSR GATK - Gather Reports job submitted with ID: {bqsr_gather_reports_job}")
    else:
      log_message("BQSR GATK - Gather Reports job submission failed")
    
    # Step 8: BQSR - GATK - ApplyBQSR
    log_message("Initiating BQSR GATK - ApplyBQSR - Job Submission")
    apply_bqsr_module = os.path.join(script_dir, "modules_slurm/bqsr/ApplyBQSR.sbatch")
    cpus, mem = get_resources(config, "applyBQSR")
    apply_bqsr_job = submit_job(
            apply_bqsr_module,
            export=f"BQSR_TABLE={gathered_report},INPUT_BAM={rmdup_bam},SAMPLEID={sampleid},REFERENCE={reference},OUTPUT_DIR={output_dir},CPUS={cpus},MEM={mem}",
            output_dir=output_dir,
            job_name="GATK-ApplyBQSR",
            dependency=bqsr_gather_reports_job,
            cpus=cpus,
            mem=mem
        )
    recalibrated_bam = os.path.join(output_dir, f"{sampleid}.recalibrated.bam")
    if apply_bqsr_job:
      log_message(f"BQSR GATK - Apply BQSR job submitted with ID: {apply_bqsr_job}")
    else:
      log_message("BQSR GATK - Apply BQSR job submission failed")
    
    # Step 9: FilterBAM - Samtools
    log_message("Initiating BAM filtration Samtools - Job Submission")
    output_dir = os.path.join(main_output_dir, "bam_preprocessing")
    filter_bam_module = os.path.join(script_dir, "modules_slurm/bam_preprocessing/FilterBAM.sbatch")
    cpus, mem = get_resources(config, "filterBAM")
    bam_filter_job = submit_job(
            filter_bam_module,
            export=f"INPUT_BAM={recalibrated_bam},SAMPLEID={sampleid},OUTPUT_DIR={output_dir},MEM={mem},CPUS={cpus}",
            output_dir=output_dir,
            job_name="BAM-Preprocessing-Samtools-Filtration",
            dependency=apply_bqsr_job,
            cpus=cpus,
            mem=mem
        )
    filtered_bam = os.path.join(output_dir, f"{sampleid}.filtered.bam")
    if bam_filter_job:
      log_message(f"Samtools-Bam Filtration job submitted with ID: {bam_filter_job}")
    else:
      log_message("Samtools-Bam Filtration job submission failed")
      
    # Step 10: Split Intervals - GATK
    log_message("Initiating Haplotype Caller - Split Intervals - Job Submission")
    output_dir = os.path.join(main_output_dir, "haplotype_caller")
    mkdir(output_dir)
    split_int_hc_module = os.path.join(script_dir, "modules_slurm/haplotype_caller/SplitIntervals.sbatch")
    nb_splits = 24
    hc_split_job = submit_job(
            split_int_hc_module,
            export=f"SAMPLEID={sampleid},OUTPUT_DIR={output_dir},REFERENCE={reference},TARGETS={kit},NB_SPLITS={nb_splits}",
            output_dir=output_dir,
            job_name="GATK-HC-Intervals",
            dependency=bam_filter_job
        )
    intervals_dir = os.path.join(output_dir, f"intervals")
    if hc_split_job:
      log_message(f"Haplotype Caller - Split Intervals job submitted with ID: {hc_split_job}")
    else:
      log_message("Haplotype Caller - Split Intervals job submission failed")
      
    # Step 11: HaplotypeCaller - GATK
    log_message("Initiating Haplotype Caller - Generate Split gVCF - Job Submission")
    hc_module = os.path.join(script_dir, "modules_slurm/haplotype_caller/HaplotypeCaller.sbatch")
    cpus, mem = get_resources(config, "hc")
    hc_job = submit_job(
            hc_module,
            export=f"INPUT_BAM={filtered_bam},SAMPLEID={sampleid},OUTPUT_DIR={output_dir},REFERENCE={reference},INTERVALS_DIR={intervals_dir},DBSNP={dbsnp},CPUS={cpus},MEM={mem}",
            output_dir=output_dir,
            job_name="GATK-HC-SplitsGVCF",
            dependency=hc_split_job,
            array="0-23",
            cpus=cpus,
            mem=mem
        )
    if hc_job:
      log_message(f"Haplotype Caller - Generate Split gVCF job submitted with ID: {hc_job}")
    else:
      log_message("Haplotype Caller - Generate Split gVCF job submission failed")
    
    # Step 12: GatherGVCFs - GATK
    log_message("Initiating Gather gVCFs - GATK - Job Submission")
    hc_gather_module = os.path.join(script_dir, "modules_slurm/haplotype_caller/GatherGVCF.sbatch")
    hc_gather_job = submit_job(
            hc_gather_module,
            export=f"INPUT_BAM={recalibrated_bam},SAMPLEID={sampleid},OUTPUT_DIR={output_dir},ARRAY_INDICES=23",
            output_dir=output_dir,
            job_name="GATK-Gather-GVCFs",
            dependency=hc_job
        )
    gvcf = os.path.join(output_dir, f"{sampleid}.g.vcf.gz")
    if hc_gather_job:
      log_message(f"GATK-Gather-GVCFs job submitted with ID: {hc_gather_job}")
    else:
      log_message("GATK-Gather-GVCFs job submission failed")
    
    # Step 13: Collect BAM QC metrics - GATK
    log_message("Initiating BAM QC metrics job - GATK")
    output_dir = os.path.join(main_output_dir, "qc")
    input_dir = os.path.join(main_output_dir, "bam_preprocessing")
    cpus, mem = get_resources(config, "bamqc")
    bamqc_module = os.path.join(script_dir, "modules_slurm/qc/bamqc.sbatch")
    bamqc_job = submit_job(
            bamqc_module,
            export=f"INPUT_FOLDER={input_dir},SAMPLEID={sampleid},OUTPUT_DIR={output_dir},REFERENCE={reference}",
            output_dir=output_dir,
            job_name="GATK-BAMQC",
            dependency=hc_gather_job,
            cpus=cpus,
            mem=mem
        )
    if bamqc_job:
      log_message(f"GATK-BAMQC job submitted with ID: {bamqc_job}")
    else:
      log_message("GATK-BAMQC job submission failed")
    
    # Step 13Bis: Collect Depth information from BAM files - Mosdepth
    log_message("Initiating BAM QC depth - Mosdepth")
    output_dir = os.path.join(main_output_dir, "qc")
    input_dir = os.path.join(main_output_dir, "bam_preprocessing")
    cpus, mem = get_resources(config, "mosdepth")
    mosdepth_module = os.path.join(script_dir, "modules_slurm/qc/Mosdepth.sbatch")
    mosdepth_job = submit_job(
            mosdepth_module,
            export=f"INPUT_FOLDER={input_dir},SAMPLEID={sampleid},OUTPUT_DIR={output_dir},TARGETS={kit},CPUS={cpus}",
            output_dir=output_dir,
            job_name="MOSDEPTH-BAMDEPTH",
            dependency=hc_gather_job,
            cpus=cpus,
            mem=mem
        )
    if mosdepth_job:
      log_message(f"MOSDEPTH-BAMDEPTH job submitted with ID: {mosdepth_job}")
    else:
      log_message("MOSDEPTH-BAMDEPTH job submission failed")
            
    # Step 14: Convert BAM to CRAM - Samtools
    log_message("Initiating Convert2Cram job 1/2 - Samtools")
    output_dir = os.path.join(main_output_dir, "bam_preprocessing/bqsr")
    convert_cram_module = os.path.join(script_dir, "modules_slurm/utils/Convert2CRAM.sbatch")
    convert_cram_job = submit_job(
            convert_cram_module,
            export=f"INPUT_BAM={recalibrated_bam},SAMPLEID={sampleid},OUTPUT_DIR={output_dir},REFERENCE={reference},BAM_TYPE=recalibrated",
            output_dir=output_dir,
            job_name="SAMTOOLS-CONVERT-CRAM",
            dependency=hc_gather_job
        )
    if convert_cram_job:
      log_message(f"SAMTOOLS-CONVERT-CRAM job submitted with ID: {convert_cram_job}")
    else:
      log_message("SAMTOOLS-CONVERT-CRAM job submission failed")
    
    # Step 15: Convert BAM to CRAM - Samtools
    log_message("Initiating Convert2Cram job 2/2 - Samtools")
    output_dir = os.path.join(main_output_dir, "bam_preprocessing")
    convert_cram_module = os.path.join(script_dir, "modules_slurm/utils/Convert2CRAM.sbatch")
    convert_cram_job_2 = submit_job(
            convert_cram_module,
            export=f"INPUT_BAM={rmdup_bam},SAMPLEID={sampleid},OUTPUT_DIR={output_dir},REFERENCE={reference},BAM_TYPE=rmdup",
            output_dir=output_dir,
            job_name="SAMTOOLS-CONVERT-CRAM",
            dependency=hc_gather_job
        )
    if convert_cram_job_2:
      log_message(f"SAMTOOLS-CONVERT-CRAM job submitted with ID: {convert_cram_job_2}")
    else:
      log_message("SAMTOOLS-CONVERT-CRAM job submission failed")
      
    # Step 16: Remove intermediary BAM - Python
    log_message("Initiating Remove intermediary Bam job")
    output_dir = main_output_dir
    erase_bam_module = os.path.join(script_dir, "modules_slurm/utils/EraseBAM.sbatch")
    erase_bam_job = submit_job(
            erase_bam_module,
            export=f"SAMPLEID={sampleid},OUTPUT_DIR={output_dir}",
            output_dir=output_dir,
            job_name="ERASE-BAM",
            dependency=f"{convert_cram_job}:{convert_cram_job_2}"
        )
    if erase_bam_job:
      log_message(f"ERASE-BAM job submitted with ID: {erase_bam_job}")
    else:
      log_message("ERASE-BAM job submission failed")
    
    # Step 17: Generate Report - MultiQC
    log_message("Initiating MultiQC job")
    output_dir = os.path.join(main_output_dir, "qc")
    input_dir = os.path.join(main_output_dir, "qc")
    multiqc_module = os.path.join(script_dir, "modules_slurm/qc/MultiQC.sbatch")
    multiqc_job = submit_job(
            multiqc_module,
            export=f"SAMPLEID={sampleid},INPUT_DIR={input_dir},OUTPUT_DIR={output_dir}",
            output_dir=output_dir,
            job_name="MultiQC",
            dependency=convert_cram_job
        )
    if multiqc_job:
      log_message(f"MultiQC job submitted with ID: {multiqc_job}")
    else:
      log_message("MultiQC job submission failed")

    log_message("Pipeline submission finished")
    
    last_job_id = multiqc_job
    
    return last_job_id
    
  except Exception as e:
    log_message(f"Error: {e}")
    

if __name__ == "__main__":

  parser = argparse.ArgumentParser(description="Run the genomic pipeline.")
  parser.add_argument("--config", required=True, help="Path to the configuration file")
  parser.add_argument("--output", required=True, help="Path to the output directory")
  parser.add_argument("--assembly", required=True, help="Assembly version [GRCh38]")
  parser.add_argument("--read1", required=True, help="Path to read 1 fastq file")
  parser.add_argument("--read2", required=True, help="Path to read 2 fastq file")
  parser.add_argument("--sample", required=True, help="Sample ID")
  parser.add_argument("--targets", required=True, help="Exome Kits [sureselectv6, nextera]")

  args = parser.parse_args()
  main(args)