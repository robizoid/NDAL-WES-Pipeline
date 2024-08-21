import os
import glob
import argparse

def find_fastq_files(input_dir):
    fastq_files = {}
    
    # Pattern 1: INPUTFOLDER/${SAMPLEID}/first/${SAMPLEID}_1.fastq.gz
    pattern1 = os.path.join(input_dir, '*', 'first', '*_1.fastq.gz')
    pattern2 = os.path.join(input_dir, '*', 'second', '*_2.fastq.gz')
    for read1 in glob.glob(pattern1):
        sampleid = os.path.basename(read1).replace('_1.fastq.gz', '')
        read2 = read1.replace('first', 'second').replace('_1.fastq.gz', '_2.fastq.gz')
        if os.path.exists(read2):
            fastq_files[sampleid] = (read1, read2)
    
    # Pattern 2: INPUTFOLDER/${SAMPLEID}/${SAMPLEID}_1.fastq.gz
    pattern3 = os.path.join(input_dir, '*', '*_1.fastq.gz')
    for read1 in glob.glob(pattern3):
        sampleid = os.path.basename(read1).replace('_1.fastq.gz', '')
        read2 = read1.replace('_1.fastq.gz', '_2.fastq.gz')
        if os.path.exists(read2):
            fastq_files[sampleid] = (read1, read2)
    
    # Pattern 3: INPUTFOLDER/${SAMPLEID}_1.fastq.gz
    pattern4 = os.path.join(input_dir, '*_1.fastq.gz')
    for read1 in glob.glob(pattern4):
        sampleid = os.path.basename(read1).replace('_1.fastq.gz', '')
        read2 = read1.replace('_1.fastq.gz', '_2.fastq.gz')
        if os.path.exists(read2):
            fastq_files[sampleid] = (read1, read2)
    
    return fastq_files

def generate_tsv(fastq_files, input_dir, output_tsv, assembly, targets):
    with open(output_tsv, 'w') as tsv_file:
        # Write header
        tsv_file.write("SAMPLEID\tREAD1\tREAD2\tOUTPUTDIR\tASSEMBLY\tTARGETS\n")
        
        for sampleid, (read1, read2) in fastq_files.items():
            outputdir = os.path.join(input_dir, "analysis", sampleid)
            # Write the sample information to the TSV file
            tsv_file.write(f"{sampleid}\t{read1}\t{read2}\t{outputdir}\t{assembly}\t{targets}\n")
    
    print(f"TSV file generated: {output_tsv}")

def main():
    parser = argparse.ArgumentParser(description="Generate a TSV file for a cohort of samples.")
    parser.add_argument('--input_dir', required=True, help="Directory containing the FASTQ files.")
    parser.add_argument('--output_tsv', default="samples.tsv", help="Output TSV file.")
    parser.add_argument('--assembly', default="GRCh38", help="Assembly version.")
    parser.add_argument('--targets', default="sureselectv6", help="Exome kit targets.")
    args = parser.parse_args()
    
    fastq_files = find_fastq_files(args.input_dir)
    if not fastq_files:
        print("No FASTQ files found matching the expected patterns.")
        return
    
    generate_tsv(fastq_files, args.input_dir, args.output_tsv, args.assembly, args.targets)

if __name__ == "__main__":
    main()
