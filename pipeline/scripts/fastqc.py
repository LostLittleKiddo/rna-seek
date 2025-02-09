from Bio import SeqIO
from Bio.Seq import Seq
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional

# Common adapter sequences (expand as needed)
ADAPTERS = [
    "AGATCGGAAGAGCACACGTCTGAACTCCAGTCA",  # TruSeq Universal Adapter
    "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT",  # TruSeq Adapter Index 1
]

# Dictionary of known overrepresented sequences (Adapters, Primers, Contaminants)
KNOWN_SEQ = {
    "TruSeq Adapter, Index 7": "AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC",
    "TruSeq Universal Adapter": "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTA",
    "TruSeq Read 1 Adapter": "AGATCGGAAGAGCGGTTCAGCAGGAATGCCGAG",
    "TruSeq Read 2 Adapter": "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT",
    "Illumina Multiplexing PCR Primer 1.0": "AATGATACGGCGACCACCGAGATCTACAC",
    "Illumina Multiplexing PCR Primer 2.0": "CAAGCAGAAGACGGCATACGAGAT",
    "Nextera Transposase Adapter": "CTGTCTCTTATACACATCT",
    "Nextera Read 1 Adapter": "TCGTCGGCAGCGTCAGATGTGTATAAGAGACAG",
    "Nextera Read 2 Adapter": "GTCTCGTGGGCTCGGAGATGTGTATAAGAGACAG",
    "PhiX Control Library": "GTTTTCCCAGTCACGACGTTG",
    "Small RNA Adapter (Read 1)": "TGGAATTCTCGGGTGCCAAGG",
    "Small RNA Adapter (Read 2)": "CTGTAGGCACCATCAATAGATCGGAAGAGCACACGTCT",
}


def generate_quality_charts(report_data: Dict, fastqc_folder: Path, file_stem: str) -> Optional[List[Path]]:
    """Generate visualizations for quality metrics."""
    try:
        fig_dir = fastqc_folder / "plots"
        fig_dir.mkdir(exist_ok=True)
        plot_paths = []

        def save_plot(fig_num: int, plot_func):
            plt.figure(figsize=(15, 12))
            plot_func()
            plot_path = fig_dir / f"{file_stem}_quality_plots{fig_num}.png"
            plt.savefig(plot_path, dpi=150, bbox_inches='tight')
            plot_paths.append(plot_path)
            plt.close()

        def create_blank_plot(title: str, message: str):
            """Create a blank plot with a centered message."""
            plt.text(0.5, 0.5, message, ha='center', va='center', fontsize=14, color='gray')
            plt.title(title)
            plt.axis('off')

        def plot_original_metrics():
            plt.subplot(2, 2, 1)
            positions = list(report_data['quality_stats'].keys())
            means = [v['mean'] for v in report_data['quality_stats'].values()]
            medians = [v['median'] for v in report_data['quality_stats'].values()]
            q25 = [v['q25'] for v in report_data['quality_stats'].values()]
            q75 = [v['q75'] for v in report_data['quality_stats'].values()]

            if positions:
                plt.plot(positions, means, label='Mean')
                plt.plot(positions, medians, label='Median')
                plt.fill_between(positions, q25, q75, alpha=0.3, label='IQR (25-75%)')
                plt.xlabel('Position in Read (bp)')
                plt.ylabel('Phred Quality Score')
                plt.title('Per-Base Sequence Quality')
                plt.legend()
                plt.grid(True)
            else:
                create_blank_plot("Per-Base Sequence Quality", "No data available")

            plt.subplot(2, 2, 2)
            if report_data['gc_content']:
                plt.hist(report_data['gc_content'], bins=np.arange(0, 101, 5), edgecolor='black', alpha=0.7)
                plt.xlabel('GC Content (%)')
                plt.ylabel('Number of Sequences')
                plt.title('GC Content Distribution')
                plt.grid(True)
            else:
                create_blank_plot("GC Content Distribution", "No data available")

            plt.subplot(2, 2, 3)
            lengths = report_data['lengths']
            if lengths:
                max_len = max(lengths)
                bins = np.linspace(0, max_len + 10, 50)
                plt.hist(lengths, bins=bins, edgecolor='black', alpha=0.7)
                plt.xlabel('Sequence Length (bp)')
                plt.ylabel('Count')
                plt.title('Sequence Length Distribution')
                plt.grid(True)
            else:
                create_blank_plot("Sequence Length Distribution", "No data available")

            plt.subplot(2, 2, 4)
            overrep = report_data.get('overrepresented', [])
            if overrep:
                sequences, counts = zip(*[(seq[:20] + '...', count) for seq, count in overrep])
                plt.barh(sequences, counts)
                plt.xlabel('Count')
                plt.title('Top Overrepresented Sequences')
                plt.gca().invert_yaxis()
            else:
                create_blank_plot("Top Overrepresented Sequences", "No overrepresented sequences (>0.1% of total)")

        def plot_new_metrics():
            plt.figure(figsize=(18, 20))
            plt.subplots_adjust(hspace=0.5, wspace=0.3)

            def plot_per_tile_quality():
                plt.subplot(3, 2, 1)
                if report_data.get('per_tile_mean'):
                    tiles = sorted(report_data['per_tile_mean'].keys())
                    if tiles:
                        positions = sorted(report_data['per_tile_mean'][tiles[0]].keys())
                        data = np.array([[report_data['per_tile_mean'][tile].get(pos, 0) for pos in positions] for tile in tiles])
                        plt.imshow(data, aspect='auto', cmap='viridis', interpolation='nearest')
                        plt.colorbar(label='Mean Quality Score')
                        plt.xlabel('Position in Read')
                        plt.ylabel('Tile')
                        plt.title('Per Tile Sequence Quality')
                        plt.xticks(np.arange(len(positions))[::10], positions[::10], rotation=45)
                        plt.yticks(np.arange(len(tiles))[::2], tiles[::2])
                    else:
                        create_blank_plot("Per Tile Sequence Quality", "No tile data available")
                else:
                    create_blank_plot("Per Tile Sequence Quality", "No tile information available")

            def plot_per_sequence_quality():
                plt.subplot(3, 2, 2)
                per_seq_qual = report_data.get('per_seq_quality', [])
                if per_seq_qual:
                    plt.hist(per_seq_qual, bins=50, edgecolor='black', alpha=0.7)
                    plt.xlabel('Average Quality Score per Read')
                    plt.ylabel('Count')
                    plt.title('Per Sequence Quality Scores')
                    plt.grid(True)
                else:
                    create_blank_plot("Per Sequence Quality Scores", "No data available")

            def plot_per_base_sequence_content():
                plt.subplot(3, 2, 3)
                if report_data.get('per_base_percent'):
                    positions = sorted(report_data['per_base_percent'].keys())
                    a = [report_data['per_base_percent'][pos].get('A', 0) for pos in positions]
                    t = [report_data['per_base_percent'][pos].get('T', 0) for pos in positions]
                    c = [report_data['per_base_percent'][pos].get('C', 0) for pos in positions]
                    g = [report_data['per_base_percent'][pos].get('G', 0) for pos in positions]
                    plt.plot(positions, a, label='A', color='green')
                    plt.plot(positions, t, label='T', color='red')
                    plt.plot(positions, c, label='C', color='blue')
                    plt.plot(positions, g, label='G', color='black')
                    plt.xlabel('Position in Read')
                    plt.ylabel('Percentage')
                    plt.title('Per Base Sequence Content')
                    plt.legend()
                    plt.grid(True)
                else:
                    create_blank_plot("Per Base Sequence Content", "No data available")

            # def plot_per_base_n_content():
            #     plt.subplot(3, 2, 4)
            #     if report_data.get('per_base_n_percent'):
            #         positions = sorted(report_data['per_base_n_percent'].keys())
            #         n_percent = [report_data['per_base_n_percent'][pos] for pos in positions]
                    
            #         # Plot the N content
            #         plt.plot(positions, n_percent, color='purple', label='N Content')
                    
            #         # Add labels and title
            #         plt.xlabel('Position in Read (bp)')
            #         plt.ylabel('Percentage of N')
            #         plt.title('Per Base N Content')
                    
            #         # Add grid for better readability
            #         plt.grid(True)
                    
            #         # Optionally, add a legend
            #         plt.legend()
            #     else:
            #         create_blank_plot("Per Base N Content", "No data available")

            def plot_adapter_content():
                plt.subplot(3, 2, 5)
                if report_data.get('adapter_percent'):
                    positions = sorted(report_data['adapter_percent'].keys())
                    adapter_percent = [report_data['adapter_percent'][pos] for pos in positions]
                    plt.plot(positions, adapter_percent, color='orange')
                    plt.xlabel('Position in Read')
                    plt.ylabel('Percentage of Reads with Adapter')
                    plt.title('Adapter Content')
                    plt.grid(True)
                else:
                    create_blank_plot("Adapter Content", "No adapter data")

            def plot_duplication_levels():
                plt.subplot(3, 2, 6)
                duplication = report_data.get('duplication_levels', {})
                if duplication and report_data.get('total_seqs', 0) > 0:
                    x = sorted(duplication.keys())
                    y = [(duplication[k] * k) / report_data['total_seqs'] * 100 for k in x]
                    plt.plot(x, y, marker='o', linestyle='-')
                    plt.xlabel('Duplication Level (Number of Occurrences)')
                    plt.ylabel('Percentage of Total Reads (%)')
                    plt.title('Sequence Duplication Levels')
                    plt.grid(True)
                else:
                    create_blank_plot("Sequence Duplication Levels", "No duplication data")

            plot_per_tile_quality()
            plot_per_sequence_quality()
            plot_per_base_sequence_content()
            plot_per_base_n_content()
            plot_adapter_content()
            plot_duplication_levels()

        save_plot(1, plot_original_metrics)
        save_plot(2, plot_new_metrics)
        return plot_paths

    except Exception as e:
        print(f"Error generating charts: {str(e)}")
        return None


def fastqc_analysis(fastq_file: Path, fastqc_folder: Path) -> None:
    """Perform comprehensive quality analysis with visualization."""
    report_data = {
        'quality_stats': defaultdict(list),
        'gc_content': [],
        'lengths': [],
        'overrepresented': [],
        'per_tile_quality': defaultdict(lambda: defaultdict(list)),
        'per_seq_quality': [],
        'per_base_content': defaultdict(lambda: {'A': 0, 'T': 0, 'C': 0, 'G': 0}),
        'per_base_n_content': defaultdict(int),
        'duplication_levels': defaultdict(int),
        'adapter_content': defaultdict(int),
        'total_seqs': 0,
    }

    try:
        sequence_cache = defaultdict(int)
        print(f"\nAnalyzing {fastq_file.name}...")
        total_sequences = sum(1 for _ in SeqIO.parse(fastq_file, "fastq"))
        processed_sequences = 0

        with open(fastq_file, "r") as handle:
            for record in SeqIO.parse(handle, "fastq"):
                seq_len = len(record)
                report_data['lengths'].append(seq_len)
                gc = (record.seq.count('G') + record.seq.count('C')) / seq_len * 100
                report_data['gc_content'].append(gc)
                quals = record.letter_annotations['phred_quality']
                avg_qual = np.mean(quals)
                report_data['per_seq_quality'].append(avg_qual)

                for pos, score in enumerate(quals):
                    report_data['quality_stats'][pos].append(score)

                seq = str(record.seq).upper()
                for pos, base in enumerate(seq):
                    if base in ['A', 'T', 'C', 'G']:
                        report_data['per_base_content'][pos][base] += 1
                    elif base == 'N':
                        report_data['per_base_n_content'][pos] += 1

                record_id = record.id
                parts = record_id.split(':')
                if len(parts) >= 5:
                    tile = parts[4]
                    for pos, score in enumerate(quals):
                        report_data['per_tile_quality'][tile][pos].append(score)

                for adapter in ADAPTERS:
                    adapter_upper = adapter.upper()
                    start = seq.find(adapter_upper)
                    if start != -1:
                        end = start + len(adapter_upper)
                        for p in range(start, end):
                            if p < seq_len:
                                report_data['adapter_content'][p] += 1
                        rc_adapter = str(Seq(adapter_upper).reverse_complement())
                        start = seq.find(rc_adapter)
                        if start != -1:
                            end = start + len(rc_adapter)
                            for p in range(start, end):
                                if p < seq_len:
                                    report_data['adapter_content'][p] += 1

                seq_str = str(record.seq)
                sequence_cache[seq_str] += 1
                processed_sequences += 1
                print(f"Progress: {processed_sequences / total_sequences * 100:.2f}%", end='\r')

        report_data['total_seqs'] = len(report_data['lengths'])
        print(f"Total Sequences: {report_data['total_seqs']}")

        quality_stats = {
            pos: {
                'mean': np.mean(scores),
                'median': np.median(scores),
                'q25': sorted(scores)[int(len(scores) * 0.25)] if scores else 0,
                'q75': sorted(scores)[int(len(scores) * 0.75)] if scores else 0
            }
            for pos, scores in report_data['quality_stats'].items()
        }
        report_data['quality_stats'] = quality_stats

        per_tile_mean = {
            tile: {pos: np.mean(scores) for pos, scores in positions.items()}
            for tile, positions in report_data['per_tile_quality'].items()
        }
        report_data['per_tile_mean'] = per_tile_mean

        per_base_percent = {
            pos: {base: (count / total) * 100 for base, count in bases.items()}
            for pos, bases in report_data['per_base_content'].items()
            if (total := sum(bases.values()) + report_data['per_base_n_content'].get(pos, 0)) > 0
        }
        report_data['per_base_percent'] = per_base_percent

        report_data['per_base_n_percent'] = {
            pos: (count / report_data['total_seqs']) * 100
            for pos, count in report_data['per_base_n_content'].items()
        }

        report_data['adapter_percent'] = {
            pos: (count / report_data['total_seqs']) * 100
            for pos, count in report_data['adapter_content'].items()
        }

        for count in sequence_cache.values():
            report_data['duplication_levels'][count] += 1

        def find_known_sequence(seq: str) -> Optional[str]:
            for name, known_seq in KNOWN_SEQ.items():
                if known_seq in seq:
                    return name
                rc_seq = str(Seq(known_seq).reverse_complement())
                if rc_seq in seq:
                    return name
            return None

        if report_data['total_seqs'] > 0:
            overrepresented_sequences = [
                (seq, count, find_known_sequence(seq) or "Unknown Overrepresented Sequence")
                for seq, count in sequence_cache.items()
                if count / report_data['total_seqs'] > 0.001
            ]
            overrepresented_sequences.sort(key=lambda x: x[1], reverse=True)
            report_data['overrepresented'] = [(seq[:50], count) for seq, count, _ in overrepresented_sequences[:10]]
        else:
            report_data['overrepresented'] = []

        report_path = fastqc_folder / f"{fastq_file.stem}_qc_report.txt"
        with open(report_path, "w") as report:
            report.write(f"FASTQ Quality Report: {fastq_file.name}\n")
            report.write("=" * 50 + "\n")
            report.write(f"Total Sequences: {report_data['total_seqs']}\n")
            report.write(f"Average Length: {np.mean(report_data['lengths']):.1f} bp\n")
            report.write(f"GC Content: {np.mean(report_data['gc_content']):.1f}%\n")
            report.write(f"Average Per Sequence Quality: {np.mean(report_data['per_seq_quality']):.1f}\n")
            report.write(f"Maximum Adapter Content: {max(report_data['adapter_percent'].values(), default=0):.2f}%\n\n")
            report.write("Overrepresented Sequences:\n")
            for seq, count in report_data['overrepresented']:
                report.write(f"Sequence: {seq}, Count: {count}, Percentage: {(count / report_data['total_seqs']) * 100:.5f}%\n")
            report.write("\n")

            plot_paths = generate_quality_charts(report_data, fastqc_folder, fastq_file.stem)
            if plot_paths:
                for i, path in enumerate(plot_paths, 1):
                    report.write(f"Quality plots part {i} saved to: {path}\n")

        print(f"\nQuality report generated: {report_path.name}")

    except Exception as e:
        print(f"Error analyzing {fastq_file.name}: {str(e)}")