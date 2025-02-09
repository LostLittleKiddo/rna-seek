import os
from pathlib import Path
import gzip

from fastqc import fastqc_analysis
from trimming import wasm_trim_reads  # Import wasm_trim_reads function


def organize_folders(folder_path, tar_folder, fastqc_folder, trimmed_folder, trimmed_fastqc_folder):
    """Create necessary directories if they don't exist."""
    try:
        for directory in [tar_folder, fastqc_folder, trimmed_folder, trimmed_fastqc_folder]:
            directory.mkdir(parents=True, exist_ok=True)

        if not folder_path.is_dir():
            print(f"Error: {folder_path} is not a valid directory.")
            return False

        return True
    except Exception as e:
        print(f"Directory creation error: {str(e)}")
        return False


def find_fastq_files(folder_path):
    """Find all FASTQ files in the directory, including compressed versions."""
    extensions = ["*.fastq", "*.fq", "*.fastq.gz", "*.fq.gz"]
    fastq_files = []
    for ext in extensions:
        fastq_files.extend(folder_path.glob(ext))

    gz_signal = any(f.suffix == ".gz" for f in fastq_files)
    return fastq_files, gz_signal


def convert_and_move_gz(fastq_files, folder_path, tar_folder):
    """Decompress gzipped files and move originals to archive folder."""
    for fastq_file in fastq_files:
        if fastq_file.suffix == ".gz":
            output_file = folder_path / fastq_file.with_suffix("").name
            try:
                with gzip.open(fastq_file, "rt") as f_in, open(output_file, "w") as f_out:
                    f_out.write(f_in.read())
                print(f"Converted {fastq_file.name} to {output_file.name}")
                tar_file = tar_folder / fastq_file.name
                fastq_file.rename(tar_file)
                print(f"Archived {fastq_file.name} to {tar_file}")
            except Exception as e:
                print(f"Error processing {fastq_file.name}: {str(e)}")


def process_single_end_reads(uncompressed_files, fastqc_folder, trimmed_folder, trimmed_fastqc_folder):
    """Process single-end reads."""
    for fastq_file in uncompressed_files:
        # Step 1: Run FastQC on raw reads
        print(f"\nRunning FastQC on {fastq_file.name}...")
        fastqc_analysis(fastq_file, fastqc_folder)

        # Step 2: Trim adapters (single-end)
        trimmed_output_file = trimmed_folder / fastq_file.name
        print(f"Trimming adapters from {fastq_file.name}...")
        wasm_trim_reads(fastq_file, trimmed_output_file)

        # Step 3: Run FastQC on trimmed reads
        print(f"Running FastQC on trimmed {fastq_file.name}...")
        fastqc_analysis(trimmed_output_file, trimmed_fastqc_folder)


def process_paired_end_reads(forward_files, reverse_files, fastqc_folder, trimmed_folder, trimmed_fastqc_folder):
    """Process paired-end reads."""
    for forward_file, reverse_file in zip(forward_files, reverse_files):
        # Step 1: Run FastQC on raw reads
        print(f"\nRunning FastQC on {forward_file.name} and {reverse_file.name}...")
        fastqc_analysis(forward_file, fastqc_folder)
        fastqc_analysis(reverse_file, fastqc_folder)

        # Step 2: Trim adapters (paired-end)
        forward_trimmed = trimmed_folder / f"trimmed_1_{forward_file.name}"
        reverse_trimmed = trimmed_folder / f"trimmed_2_{reverse_file.name}"
        print(f"Trimming adapters from {forward_file.name} and {reverse_file.name}...")
        wasm_trim_reads(forward_file, forward_trimmed)
        wasm_trim_reads(reverse_file, reverse_trimmed)

        # Step 3: Run FastQC on trimmed reads
        print(f"Running FastQC on trimmed {forward_file.name} and {reverse_file.name}...")
        fastqc_analysis(forward_trimmed, trimmed_fastqc_folder)
        fastqc_analysis(reverse_trimmed, trimmed_fastqc_folder)


def main():
    """Main workflow controller."""
    # Configure paths
    folder_path = Path(os.path.join("..", "data/fastq_files"))
    output_path = Path(os.path.join("..", "data/output"))
    tar_folder = folder_path / "compressed_archive"
    trimmed_folder = output_path / "trimmed_reads"
    fastqc_folder = output_path / "quality_reports"
    trimmed_fastqc_folder = output_path / "trimmed_reports"

    # Initialize directory structure
    if not organize_folders(folder_path, tar_folder, fastqc_folder, trimmed_folder, trimmed_fastqc_folder):
        return

    # Find all FASTQ files
    fastq_files, gz_signal = find_fastq_files(folder_path)

    if not fastq_files:
        print("No FASTQ files found (*.fastq, *.fq, or *.gz versions).")
        return

    print(f"\nFound {len(fastq_files)} FASTQ file(s) in {folder_path}")

    # Process compressed files if found
    if gz_signal:
        print("\nProcessing compressed files...")
        convert_and_move_gz(fastq_files, folder_path, tar_folder)

    # Process all uncompressed FASTQ files
    print("\nRunning quality analysis...")
    uncompressed_files = list(folder_path.glob("*.fastq")) + list(folder_path.glob("*.fq"))

    # Check if paired-end or single-end reads
    if len(uncompressed_files) % 2 == 0:  # Paired-end assumption
        forward_files = sorted([f for f in uncompressed_files if "_R1" in f.name])
        reverse_files = sorted([f for f in uncompressed_files if "_R2" in f.name])

        if len(forward_files) != len(reverse_files):
            print("Error: Mismatch between forward and reverse files.")
            return

        process_paired_end_reads(forward_files, reverse_files, fastqc_folder, trimmed_folder, trimmed_fastqc_folder)
    else:  # Single-end assumption
        process_single_end_reads(uncompressed_files, fastqc_folder, trimmed_folder, trimmed_fastqc_folder)

    print("\nProcessing complete!")


if __name__ == '__main__':
    main()