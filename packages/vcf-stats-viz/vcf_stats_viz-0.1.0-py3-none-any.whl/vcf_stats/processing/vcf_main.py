import sys
import pandas as pd
import logging
import os
import time
import psutil
import threading
from typing import Tuple, Dict, Any, Optional, List
from .vcf_parser_utils import parse_vcf_complete_optimized, read_vcf_direct_traditional
from .vcf_parser import UniversalVCFParser
from .vcf_file_io import save_analysis_results, detect_info_fields_and_size

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MemoryMonitor:
    """Monitors maximum RAM usage in real time."""

    def __init__(self, interval_seconds: float = 0.1):
        """
        Args:
            interval_seconds: Interval between measurements (seconds)
        """
        self.process = psutil.Process(os.getpid())
        self.interval = interval_seconds
        self.max_memory_mb = 0
        self.min_memory_mb = float('inf')
        self.avg_memory_mb = 0
        self.samples = 0
        self.memory_samples: List[float] = []
        self.running = False
        self.thread = None
        self.start_time = None

    def _monitor_loop(self):
        """Background monitoring loop."""
        while self.running:
            try:
                current_mb = self.get_current_memory_mb()

                self.max_memory_mb = max(self.max_memory_mb, current_mb)
                self.min_memory_mb = min(self.min_memory_mb, current_mb)
                self.memory_samples.append(current_mb)
                self.samples += 1

                time.sleep(self.interval)
            except Exception:
                break

    def get_current_memory_mb(self) -> float:
        """Get current memory usage in MB."""
        try:
            return self.process.memory_info().rss / (1024 * 1024)
        except Exception:
            return 0.0

    def start(self) -> float:
        """Start background monitoring."""
        if self.running:
            return self.max_memory_mb

        self.running = True
        self.start_time = time.time()
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()

        time.sleep(0.01)
        initial_mb = self.get_current_memory_mb()
        self.max_memory_mb = initial_mb
        self.min_memory_mb = initial_mb
        self.memory_samples.append(initial_mb)
        self.samples = 1

        logger.info(f"Memory monitor started: {initial_mb:.1f} MB initial")
        return initial_mb

    def stop(self) -> dict:
        """Stop monitoring and return statistics."""
        if not self.running:
            return {}

        self.running = False
        if self.thread:
            self.thread.join(timeout=2)

        if self.memory_samples:
            self.avg_memory_mb = sum(self.memory_samples) / len(self.memory_samples)

        duration = time.time() - self.start_time if self.start_time else 0

        stats = {
            'max_memory_mb': round(self.max_memory_mb, 2),
            'min_memory_mb': round(self.min_memory_mb, 2),
            'avg_memory_mb': round(self.avg_memory_mb, 2),
            'peak_memory_mb': round(self.max_memory_mb, 2),
            'samples_taken': self.samples,
            'measurement_duration': round(duration, 2),
            'measurement_interval_ms': self.interval * 1000,
            'memory_samples': self.memory_samples[:1000]
        }

        logger.info(f"Monitor stopped. Peak: {stats['peak_memory_mb']:.1f} MB")
        return stats

    def get_peak_memory(self) -> float:
        """Get measured memory peak."""
        return round(self.max_memory_mb, 2)

    def print_realtime_update(self, interval_seconds: float = 5.0):
        """Print periodic memory updates (optional)."""
        if not self.running:
            return

        def print_updates():
            last_print = time.time()
            while self.running:
                current_time = time.time()
                if current_time - last_print >= interval_seconds:
                    current_mb = self.get_current_memory_mb()
                    print(f"Current memory: {current_mb:.1f} MB | Peak: {self.max_memory_mb:.1f} MB")
                    last_print = current_time
                time.sleep(1.0)

        update_thread = threading.Thread(target=print_updates, daemon=True)
        update_thread.start()


def comprehensive_analysis_complete_optimized(file_path: str, max_variants: Optional[int] = None,
                                              chunk_size: int = 50000, save_results: bool = True,
                                              output_dir: str = "vcf_analysis_results") -> Tuple[
    pd.DataFrame, Dict[str, Any], Dict[str, str]]:
    """
    Complete VCF analysis with memory peak measurement.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return pd.DataFrame(), {}, {}

    print(f"\n{'=' * 80}")
    print(f"COMPLETE LOAD WITH MEMORY MONITORING")
    print(f"{'=' * 80}")

    print("Starting RAM memory monitor...")
    memory_monitor = MemoryMonitor(interval_seconds=0.05)
    initial_memory = memory_monitor.start()
    memory_monitor.print_realtime_update(interval_seconds=3.0)

    print(f"Initial memory: {initial_memory:.1f} MB")
    print(f"Monitoring every: {memory_monitor.interval * 1000:.0f} ms")

    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    info_fields, file_info = detect_info_fields_and_size(file_path, sample_lines=5000)

    print(f"\nFile: {os.path.basename(file_path)}")
    print(f"Size: {file_size_mb:.1f} MB")
    print(f"Chunk size: {chunk_size:,} variants")
    print(f"INFO fields detected: {len(info_fields)}")
    if max_variants:
        print(f"Limit: {max_variants:,} variants")

    print(f"\nLoading data with real-time memory measurement...")
    print("-" * 60)

    start_load_time = time.time()

    try:
        df = parse_vcf_complete_optimized(
            file_path=file_path,
            max_variants=max_variants,
            chunk_size=chunk_size,
            optimize_memory=True
        )

        print(f"DataFrame loaded ({len(df):,} rows) - will be automatically sorted when saving")

    except Exception as e:
        memory_stats = memory_monitor.stop()
        print(f"\nError during loading: {e}")
        print(f"Memory peak reached: {memory_stats.get('peak_memory_mb', 0):.1f} MB")
        import traceback
        traceback.print_exc()
        return pd.DataFrame(), {}, {}

    load_time = time.time() - start_load_time

    memory_stats = memory_monitor.stop()

    if df.empty:
        print("Error: Could not load data")
        print(f"Memory peak: {memory_stats.get('peak_memory_mb', 0):.1f} MB")
        return pd.DataFrame(), {}, {}

    start_stats_time = time.time()
    parser = UniversalVCFParser()
    summary = parser.get_comprehensive_summary(df)
    stats_time = time.time() - start_stats_time

    summary.update({
        'memory_stats_detailed': {
            'peak_memory_mb': memory_stats['peak_memory_mb'],
            'initial_memory_mb': round(initial_memory, 2),
            'final_memory_mb': round(memory_monitor.get_current_memory_mb(), 2),
            'memory_increase_mb': round(memory_stats['peak_memory_mb'] - initial_memory, 2),
            'min_memory_mb': memory_stats['min_memory_mb'],
            'avg_memory_mb': memory_stats['avg_memory_mb'],
            'samples_taken': memory_stats['samples_taken'],
            'measurement_interval_ms': memory_monitor.interval * 1000,
            'memory_samples_count': len(memory_stats.get('memory_samples', []))
        },
        'processing_stats': {
            'load_time_seconds': round(load_time, 2),
            'stats_time_seconds': round(stats_time, 2),
            'total_time_seconds': round(load_time + stats_time, 2),
            'load_speed_vps': round(len(df) / load_time, 0) if load_time > 0 else 0,
            'chunk_size_used': chunk_size,
            'file_size_mb': round(file_size_mb, 1),
            'sorting_note': 'Data will be automatically sorted when saving'
        },
        'memory_measurement_method': 'real_time_monitoring',
        'memory_peak_reliable': True,
        'processing_mode': 'optimized_dask_with_auto_sorting'
    })

    print(f"\n{'=' * 80}")
    print(f"PROCESSING COMPLETED")
    print(f"{'=' * 80}")

    print(f"MEMORY STATISTICS:")
    print(f"  • Peak RAM: {memory_stats['peak_memory_mb']:.1f} MB")
    print(f"  • Initial memory: {initial_memory:.1f} MB")
    print(f"  • Maximum increase: {memory_stats['peak_memory_mb'] - initial_memory:.1f} MB")
    print(f"  • Minimum recorded: {memory_stats['min_memory_mb']:.1f} MB")
    print(f"  • Average: {memory_stats['avg_memory_mb']:.1f} MB")
    print(f"  • Samples taken: {memory_stats['samples_taken']:,}")

    print(f"\nTIME STATISTICS:")
    print(f"  • Load time: {load_time:.1f} seconds")
    print(f"  • Statistics time: {stats_time:.1f} seconds")
    print(f"  • Total: {load_time + stats_time:.1f} seconds")
    if load_time > 0:
        print(f"  • Speed: {len(df) / load_time:.0f} variants/second")

    print(f"\nANALYSIS RESULTS:")
    print(f"  • Variants loaded: {len(df):,}")
    print(f"  • Chromosomes: {len(summary['chromosome_counts'])}")
    print(f"  • Variant types: {len(summary['variant_type_counts'])}")

    if 'quality_stats' in summary and 'mean' in summary['quality_stats']:
        print(f"  • Average quality: {summary['quality_stats']['mean']:.2f}")

    bytes_per_variant = (memory_stats['peak_memory_mb'] * 1024 * 1024) / len(df) if len(df) > 0 else 0
    print(f"  • Memory efficiency: {bytes_per_variant:.1f} bytes/variant")

    print(f"\nPROCESSING NOTE:")
    print(f"  • Data processed with Dask for maximum efficiency")
    print(f"  • Will be automatically sorted by position when saving")

    saved_files = {}
    if save_results:
        print(f"\nSaving results (sorting by position)...")
        try:
            saved_files = save_analysis_results(df, summary, output_dir)
            print(f"Results saved and sorted in: {output_dir}")
        except Exception as e:
            print(f"Error saving results: {e}")

    peak_mb = memory_stats['peak_memory_mb']

    print(f"\n{'=' * 80}")
    print(f"FINAL SUMMARY")
    print(f"{'=' * 80}")

    if peak_mb > 8000:
        print(f"ALERT: Extremely high memory peak ({peak_mb:.0f} MB)")
        print(f"  • Consider increasing --chunk-size for larger files")
        print(f"  • Your system might have issues with files > {file_size_mb * 2:.0f} MB")
    elif peak_mb > 4000:
        print(f"WARNING: High memory peak ({peak_mb:.0f} MB)")
        print(f"  • For better performance, use --chunk-size {chunk_size * 2:,}")
    else:
        print(f"Memory within reasonable limits ({peak_mb:.0f} MB)")

    if not df.empty:
        print(f"\nSAMPLE (3 of {len(df):,}):")
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        print(df.head(3))
        pd.reset_option('display.max_columns')
        pd.reset_option('display.width')

    print(f"\nRECOMMENDATION FOR NEXT EXECUTION:")
    print(f"  python vcf_main.py {file_path} --chunk-size {max(10000, chunk_size)}")

    return df, summary, saved_files


def benchmark_traditional_method(file_path: str, max_variants: Optional[int] = None) -> Tuple[
    pd.DataFrame, Dict[str, Any]]:
    """
    Benchmark of traditional method for comparison.
    """
    print(f"\nBENCHMARK: Traditional method (no optimization)")

    memory_monitor = MemoryMonitor(interval_seconds=0.05)
    initial_memory = memory_monitor.start()

    start_time = time.time()

    try:
        df = read_vcf_direct_traditional(file_path, max_variants)
    except Exception as e:
        memory_stats = memory_monitor.stop()
        print(f"Error in traditional benchmark: {e}")
        return pd.DataFrame(), {}

    load_time = time.time() - start_time
    memory_stats = memory_monitor.stop()

    if df.empty:
        print("Could not load data in traditional benchmark")
        return pd.DataFrame(), {}

    parser = UniversalVCFParser()
    summary = parser.get_comprehensive_summary(df)

    summary['benchmark_info'] = {
        'method': 'traditional',
        'load_time_seconds': round(load_time, 2),
        'peak_memory_mb': memory_stats['peak_memory_mb'],
        'initial_memory_mb': round(initial_memory, 2),
        'memory_increase_mb': round(memory_stats['peak_memory_mb'] - initial_memory, 2)
    }

    print(f"  • Time: {load_time:.1f} seconds")
    print(f"  • Memory peak: {memory_stats['peak_memory_mb']:.1f} MB")
    print(f"  • Variants: {len(df):,}")

    return df, summary


def main():
    """
    Main entry point.
    """
    if len(sys.argv) > 1:
        file_path = sys.argv[1]

        max_variants = None
        save_results = True
        output_dir = "vcf_analysis_results"
        chunk_size = 50000
        benchmark = False

        i = 2
        while i < len(sys.argv):
            arg = sys.argv[i]

            if arg == '--max-variants' and i + 1 < len(sys.argv):
                try:
                    max_variants = int(sys.argv[i + 1])
                    i += 2
                    continue
                except ValueError:
                    print(f"Error: '{sys.argv[i + 1]}' is not a valid number")
                    return

            elif arg == '--chunk-size' and i + 1 < len(sys.argv):
                try:
                    chunk_size = int(sys.argv[i + 1])
                    i += 2
                    continue
                except ValueError:
                    print(f"Error: '{sys.argv[i + 1]}' is not a valid number")
                    return

            elif arg == '--no-save':
                save_results = False
                i += 1
                continue

            elif arg == '--output-dir' and i + 1 < len(sys.argv):
                output_dir = sys.argv[i + 1]
                i += 2
                continue

            elif arg == '--benchmark':
                benchmark = True
                i += 1
                continue

            elif arg == '--simple':
                print("Simple mode activated (no memory optimization)")
                return run_simple_mode(file_path, max_variants, save_results, output_dir)

            else:
                try:
                    max_variants = int(arg)
                    i += 1
                    continue
                except ValueError:
                    print(f"Unrecognized argument: {arg}")
                    i += 1
                    continue

        if benchmark:
            print(f"\n{'=' * 80}")
            print(f"RUNNING COMPARATIVE BENCHMARK")
            print(f"{'=' * 80}")

            df_trad, summary_trad = benchmark_traditional_method(file_path, max_variants)

            print(f"\n{'=' * 80}")

            df_opt, summary_opt, _ = comprehensive_analysis_complete_optimized(
                file_path=file_path,
                max_variants=max_variants,
                chunk_size=chunk_size,
                save_results=False,
                output_dir=output_dir
            )

            if not df_trad.empty and not df_opt.empty:
                print(f"\n{'=' * 80}")
                print(f"RESULTS COMPARISON")
                print(f"{'=' * 80}")

                time_improvement = 0
                mem_improvement = 0

                if 'benchmark_info' in summary_trad and 'processing_stats' in summary_opt:
                    trad_time = summary_trad['benchmark_info']['load_time_seconds']
                    opt_time = summary_opt['processing_stats']['load_time_seconds']
                    trad_mem = summary_trad['benchmark_info']['peak_memory_mb']
                    opt_mem = summary_opt['memory_stats_detailed']['peak_memory_mb']

                    time_improvement = ((trad_time - opt_time) / trad_time * 100) if trad_time > 0 else 0
                    mem_improvement = ((trad_mem - opt_mem) / trad_mem * 100) if trad_mem > 0 else 0

                print(f"  • Time improvement: {time_improvement:+.1f}%")
                print(f"  • Memory improvement: {mem_improvement:+.1f}%")
                print(f"  • Variants processed: {len(df_opt):,}")

        else:
            df, summary, saved_files = comprehensive_analysis_complete_optimized(
                file_path=file_path,
                max_variants=max_variants,
                chunk_size=chunk_size,
                save_results=save_results,
                output_dir=output_dir
            )

    else:
        print("USAGE: python vcf_main.py <vcf_file_path> [options]")
        print("\nOPTIONS:")
        print("  --max-variants N    Limit to N variants")
        print("  --chunk-size N      Chunk size (default: 50000)")
        print("  --no-save           Do not save results to disk")
        print("  --output-dir DIR    Output directory for results")
        print("  --benchmark         Run comparative benchmark")
        print("  --simple            Simple mode (no optimization)")
        print("\nPERFORMANCE:")
        print("  • Real-time RAM memory monitoring")
        print("  • Measures maximum RAM peak during processing")
        print("  • Automatic recommendations based on memory usage")
        print("\nEXAMPLES:")
        print("  python vcf_main.py data.vcf")
        print("  python vcf_main.py large_data.vcf --chunk-size 100000")
        print("  python vcf_main.py data.vcf --benchmark")
        print("  python vcf_main.py data.vcf --max-variants 1000000 --no-save")


def run_simple_mode(file_path: str, max_variants: Optional[int],
                    save_results: bool, output_dir: str):
    """
    Simple mode for testing or small files.
    """
    print(f"\nSIMPLE MODE (no optimization)")

    parser = UniversalVCFParser()

    print(f"Loading: {os.path.basename(file_path)}")

    df = parse_vcf_complete_optimized(
        file_path,
        max_variants,
        chunk_size=10000,
        optimize_memory=False
    )

    if not df.empty:
        print(f"Loaded {len(df):,} variants")
        summary = parser.get_comprehensive_summary(df)

        print(f"\nSUMMARY:")
        print(f"• Total: {summary['total_variants']:,}")
        print(f"• Memory: {summary['memory_usage_mb']} MB")

        if save_results:
            saved_files = save_analysis_results(df, summary, output_dir)
            print(f"Saved in: {output_dir}")

        return df, summary, {}

    return pd.DataFrame(), {}, {}


if __name__ == "__main__":
    main()