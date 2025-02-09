from Bio import SeqIO

def wasm_trim_reads(input_fastq, output_fastq, min_length=36, quality_threshold=20):
    """
    WASM-friendly FASTQ trimmer using pure Python (no subprocess or external binaries).
    """
    with open(output_fastq, "w") as out_handle:
        for record in SeqIO.parse(input_fastq, "fastq"):
            if min(record.letter_annotations["phred_quality"]) >= quality_threshold:
                if len(record.seq) >= min_length:
                    SeqIO.write(record, out_handle, "fastq")


# # Define adapter sequences
# adapters_forward = [
#     "TACACTCTTTCCCTACACGACGCTCTTCCGATCT",  # PrefixPE/1
#     "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTA"   # PE1_rc
# ]
# adapters_reverse = [
#     "GTGACTGGAGTTCAGACGTGTGCTCTTCCGATCT",  # PrefixPE/2
#     "AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC"   # PE2_rc
# ]

# def trim_adapter(sequence, qualities, adapters):
#     """
#     Trims adapter sequences from a given sequence.
    
#     Parameters:
#     - sequence: The sequence to trim.
#     - qualities: The quality scores corresponding to the sequence.
#     - adapters: List of adapter sequences to check for trimming.
    
#     Returns:
#     - Tuple of trimmed sequence and trimmed qualities.
#     """
#     trimmed_seq = sequence
#     trimmed_qualities = qualities
#     for adapter in adapters:
#         adapter_pos = trimmed_seq.find(adapter)
#         if adapter_pos != -1:
#             trimmed_seq = trimmed_seq[:adapter_pos]
#             trimmed_qualities = trimmed_qualities[:adapter_pos]
#     return trimmed_seq, trimmed_qualities

# def trim_single_end(input_file, output_file, adapter_sequence, minimum_length=20):
#     """
#     Trims adapter sequences from single-end RNA sequencing reads.
    
#     Parameters:
#     - input_file: Path to the input FASTQ file.
#     - output_file: Path to the output FASTQ file after trimming.
#     - adapter_sequence: The adapter sequence to be trimmed.
#     - minimum_length: Minimum length of reads to keep after trimming (default: 20).
    
#     Returns:
#     - None
#     """
#     try:
#         with open(input_file, "r") as infile, open(output_file, "w") as outfile:
#             for record in SeqIO.parse(infile, "fastq"):
#                 sequence = record.seq
#                 qualities = record.letter_annotations["phred_quality"]
                
#                 # Trim adapter
#                 trimmed_sequence, trimmed_qualities = trim_adapter(sequence, qualities, [adapter_sequence])
                
#                 # Write trimmed read if it meets the minimum length
#                 if len(trimmed_sequence) >= minimum_length:
#                     record.seq = trimmed_sequence
#                     record.letter_annotations["phred_quality"] = trimmed_qualities
#                     SeqIO.write(record, outfile, "fastq")
        
#         print(f"Single-end trimming completed successfully. Output saved to {output_file}")
#     except Exception as e:
#         print(f"Error during single-end trimming: {e}")

# def trim_paired_end(forward_input, reverse_input, forward_output, reverse_output, minimum_length=20):
#     """
#     Trims adapter sequences from paired-end RNA sequencing reads.
    
#     Parameters:
#     - forward_input: Path to the forward input FASTQ file.S
#     - reverse_input: Path to the reverse input FASTQ file.
#     - forward_output: Path to the forward output FASTQ file after trimming.
#     - reverse_output: Path to the reverse output FASTQ file after trimming.
#     - minimum_length: Minimum length of reads to keep after trimming (default: 20).
    
#     Returns:
#     - None
#     """
#     try:
#         with open(forward_input, "r") as fin, open(reverse_input, "r") as rin, \
#              open(forward_output, "w") as fout, open(reverse_output, "w") as rout:
            
#             for forward_record, reverse_record in zip(SeqIO.parse(fin, "fastq"), SeqIO.parse(rin, "fastq")):
#                 # Trim forward read
#                 forward_seq = forward_record.seq
#                 forward_qualities = forward_record.letter_annotations["phred_quality"]
#                 forward_trimmed_seq, forward_trimmed_qualities = trim_adapter(forward_seq, forward_qualities, adapters_forward)
                
#                 # Trim reverse read
#                 reverse_seq = reverse_record.seq
#                 reverse_qualities = reverse_record.letter_annotations["phred_quality"]
#                 reverse_trimmed_seq, reverse_trimmed_qualities = trim_adapter(reverse_seq, reverse_qualities, adapters_reverse)
                
#                 # Write trimmed reads if they meet the minimum length
#                 if len(forward_trimmed_seq) >= minimum_length and len(reverse_trimmed_seq) >= minimum_length:
#                     # Update forward record
#                     forward_record.seq = forward_trimmed_seq
#                     forward_record.letter_annotations["phred_quality"] = forward_trimmed_qualities
                    
#                     # Update reverse record
#                     reverse_record.seq = reverse_trimmed_seq
#                     reverse_record.letter_annotations["phred_quality"] = reverse_trimmed_qualities
                    
#                     # Write trimmed records to output files
#                     SeqIO.write(forward_record, fout, "fastq")
#                     SeqIO.write(reverse_record, rout, "fastq")
        
#         print(f"Paired-end trimming completed successfully. Outputs saved to {forward_output} and {reverse_output}")
#     except Exception as e:
#         print(f"Error during paired-end trimming: {e}")
# # Define adapter sequences
# adapters_forward = [
#     "TACACTCTTTCCCTACACGACGCTCTTCCGATCT",  # PrefixPE/1
#     "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTA"   # PE1_rc
# ]
# adapters_reverse = [
#     "GTGACTGGAGTTCAGACGTGTGCTCTTCCGATCT",  # PrefixPE/2
#     "AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC"   # PE2_rc
# ]

# def trim_adapter(sequence, qualities, adapters):
#     """
#     Trims adapter sequences from a given sequence.
    
#     Parameters:
#     - sequence: The sequence to trim.
#     - qualities: The quality scores corresponding to the sequence.
#     - adapters: List of adapter sequences to check for trimming.
    
#     Returns:
#     - Tuple of trimmed sequence and trimmed qualities.
#     """
#     trimmed_seq = sequence
#     trimmed_qualities = qualities
#     for adapter in adapters:
#         adapter_pos = trimmed_seq.find(adapter)
#         if adapter_pos != -1:
#             trimmed_seq = trimmed_seq[:adapter_pos]
#             trimmed_qualities = trimmed_qualities[:adapter_pos]
#     return trimmed_seq, trimmed_qualities

# def trim_single_end(input_file, output_file, adapter_sequence, minimum_length=20):
#     """
#     Trims adapter sequences from single-end RNA sequencing reads.
    
#     Parameters:
#     - input_file: Path to the input FASTQ file.
#     - output_file: Path to the output FASTQ file after trimming.
#     - adapter_sequence: The adapter sequence to be trimmed.
#     - minimum_length: Minimum length of reads to keep after trimming (default: 20).
    
#     Returns:
#     - None
#     """
#     try:
#         with open(input_file, "r") as infile, open(output_file, "w") as outfile:
#             for record in SeqIO.parse(infile, "fastq"):
#                 sequence = record.seq
#                 qualities = record.letter_annotations["phred_quality"]
                
#                 # Trim adapter
#                 trimmed_sequence, trimmed_qualities = trim_adapter(sequence, qualities, [adapter_sequence])
                
#                 # Write trimmed read if it meets the minimum length
#                 if len(trimmed_sequence) >= minimum_length:
#                     record.seq = trimmed_sequence
#                     record.letter_annotations["phred_quality"] = trimmed_qualities
#                     SeqIO.write(record, outfile, "fastq")
        
#         print(f"Single-end trimming completed successfully. Output saved to {output_file}")
#     except Exception as e:
#         print(f"Error during single-end trimming: {e}")

# def trim_paired_end(forward_input, reverse_input, forward_output, reverse_output, minimum_length=20):
#     """
#     Trims adapter sequences from paired-end RNA sequencing reads.
    
#     Parameters:
#     - forward_input: Path to the forward input FASTQ file.
#     - reverse_input: Path to the reverse input FASTQ file.
#     - forward_output: Path to the forward output FASTQ file after trimming.
#     - reverse_output: Path to the reverse output FASTQ file after trimming.
#     - minimum_length: Minimum length of reads to keep after trimming (default: 20).
    
#     Returns:
#     - None
#     """
#     try:
#         with open(forward_input, "r") as fin, open(reverse_input, "r") as rin, \
#              open(forward_output, "w") as fout, open(reverse_output, "w") as rout:
            
#             for forward_record, reverse_record in zip(SeqIO.parse(fin, "fastq"), SeqIO.parse(rin, "fastq")):
#                 # Trim forward read
#                 forward_seq = forward_record.seq
#                 forward_qualities = forward_record.letter_annotations["phred_quality"]
#                 forward_trimmed_seq, forward_trimmed_qualities = trim_adapter(forward_seq, forward_qualities, adapters_forward)
                
#                 # Trim reverse read
#                 reverse_seq = reverse_record.seq
#                 reverse_qualities = reverse_record.letter_annotations["phred_quality"]
#                 reverse_trimmed_seq, reverse_trimmed_qualities = trim_adapter(reverse_seq, reverse_qualities, adapters_reverse)
                
#                 # Write trimmed reads if they meet the minimum length
#                 if len(forward_trimmed_seq) >= minimum_length and len(reverse_trimmed_seq) >= minimum_length:
#                     # Update forward record
#                     forward_record.seq = forward_trimmed_seq
#                     forward_record.letter_annotations["phred_quality"] = forward_trimmed_qualities
                    
#                     # Update reverse record
#                     reverse_record.seq = reverse_trimmed_seq
#                     reverse_record.letter_annotations["phred_quality"] = reverse_trimmed_qualities
                    
#                     # Write trimmed records to output files
#                     SeqIO.write(forward_record, fout, "fastq")
#                     SeqIO.write(reverse_record, rout, "fastq")
        
#         print(f"Paired-end trimming completed successfully. Outputs saved to {forward_output} and {reverse_output}")
#     except Exception as e:
#         print(f"Error during paired-end trimming: {e}")