import sys
import os
import argparse
import logging
import json
import glob
from typing import Optional

# Relative imports from the package structure
try:
    from .processing.vcf_main import comprehensive_analysis_complete_optimized
    from .processing.vcf_parser_utils import parse_vcf_complete_optimized
except ImportError:
    # Fallback or pass if modules are not yet loaded in specific contexts
    pass

from .visualization.vcf_web_dashboard import VCFWebDashboard
from .visualization.vcf_web_main import initialize_dashboard
from .visualization.vcf_web_data import discover_analyses

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VCFPipeline:
    """Complete pipeline for VCF analysis and visualization."""

    def __init__(self):
        self.parser_results = {}
        self.dashboard = None

    def analyze_vcf(self, vcf_file: str, max_variants: Optional[int] = None,
                    output_dir: str = "vcf_analysis_results",
                    chunk_size: int = 50000):
        """Analyze VCF file and generate results."""

        print(f"\n{'=' * 80}")
        print(f"STARTING VCF ANALYSIS")
        print(f"{'=' * 80}")
        print(f"File: {vcf_file}")
        print(f"Chunk size: {chunk_size:,} variants")
        print(f"Limit: {max_variants if max_variants else 'All variants'}")
        print(f"Output directory: {output_dir}")
        print(f"{'=' * 80}\n")

        if not os.path.exists(vcf_file):
            logger.error(f"Error: File {vcf_file} does not exist")
            return None, None, None

        try:
            # Call the optimized analysis function from the processing module
            df, summary, saved_files = comprehensive_analysis_complete_optimized(
                vcf_file, max_variants, chunk_size=chunk_size,
                save_results=True, output_dir=output_dir
            )
            processing_mode = "optimized_chunking"

        except Exception as e:
            logger.error(f"Error during analysis: {e}")
            import traceback
            traceback.print_exc()
            return None, None, None

        self.parser_results = {
            'dataframe': df,
            'summary': summary,
            'saved_files': saved_files,
            'output_dir': output_dir,
            'processing_mode': processing_mode
        }

        return df, summary, saved_files

    def launch_web_dashboard(self, output_dir: str = "vcf_analysis_results",
                             host: str = "127.0.0.1", port: int = 5000,
                             open_browser: bool = True):
        """Launch web dashboard."""

        print(f"\n{'=' * 80}")
        print(f"STARTING WEB DASHBOARD")
        print(f"{'=' * 80}")
        print(f"Data directory: {output_dir}")
        print(f"URL: http://{host}:{port}")
        print(f"{'=' * 80}\n")

        try:
            # 1. Create Dashboard instance
            self.dashboard = VCFWebDashboard(
                results_dir=output_dir,
                host=host,
                port=port
            )

            # 2. Initialize using the helper from visualization module
            # This handles templates, static files and route setup
            initialize_dashboard(self.dashboard, open_browser=open_browser)

            # 3. Start the server
            self.dashboard.run_server(debug=False)

        except Exception as e:
            logger.error(f"Error running dashboard: {e}")
            import traceback
            traceback.print_exc()

    def run_complete_pipeline(self, vcf_file: str, max_variants: Optional[int] = None,
                              output_dir: str = "vcf_analysis_results",
                              chunk_size: int = 50000,
                              launch_dashboard: bool = True,
                              dashboard_host: str = "127.0.0.1",
                              dashboard_port: int = 5000):
        """Run complete pipeline: analysis + visualization."""

        df, summary, saved_files = self.analyze_vcf(
            vcf_file, max_variants, output_dir, chunk_size=chunk_size
        )

        if df is None and summary is None:
            print("Could not complete analysis. Pipeline stopped.")
            return

        if launch_dashboard:
            self.launch_web_dashboard(
                output_dir=output_dir,
                host=dashboard_host,
                port=dashboard_port,
                open_browser=True
            )

        return df, summary, saved_files


def list_available_analyses(output_dir: str = "vcf_analysis_results"):
    """List available analyses in directory."""
    if not os.path.exists(output_dir):
        print(f"Directory {output_dir} does not exist")
        return

    print(f"\nAvailable analyses in: {output_dir}")
    print("-" * 80)

    try:
        # Use discover_analyses from visualization module to avoid code duplication
        analyses = discover_analyses(output_dir)

        if not analyses:
            print("No analyses found")
            return

        for analysis in analyses:
            print(f"{analysis['id']}")
            print(f"  Name: {analysis['name']}")
            print(f"  Variants: {analysis['total_variants']:,}")
            print(f"  Date: {analysis['date']}")
            print(f"  Mode: {analysis.get('processing_mode', 'unknown')}")
            print()

        print(f"Total: {len(analyses)} analyses found")

    except Exception as e:
        logger.error(f"Error listing analyses: {e}")


def clean_results_directory(output_dir: str = "vcf_analysis_results",
                            keep_last: int = 5):
    """Clean results directory, keeping the latest analyses."""
    if not os.path.exists(output_dir):
        print(f"Directory {output_dir} does not exist")
        return

    metadata_files = glob.glob(os.path.join(output_dir, "metadata_*.json"))

    if len(metadata_files) <= keep_last:
        print(f"Only {len(metadata_files)} analyses, nothing to clean")
        return

    # Sort by modification time
    metadata_files.sort(key=os.path.getmtime)

    # Files to delete (all except last N)
    files_to_delete = metadata_files[:-keep_last]

    print(f"\nCleaning directory: {output_dir}")
    print(f"Keeping last {keep_last} analyses")
    print(f"Deleting {len(files_to_delete)} old analyses")
    print("-" * 80)

    deleted_count = 0
    for metadata_file in files_to_delete:
        try:
            # Read metadata to find related files
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            # Delete related files
            for file_type, file_path in metadata.get('output_files', {}).items():
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"  Deleted: {os.path.basename(file_path)}")

            # Delete metadata file
            os.remove(metadata_file)
            deleted_count += 1

        except Exception as e:
            print(f"Error deleting analysis for {metadata_file}: {e}")

    print(f"\nCleanup completed: {deleted_count} analyses deleted")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Complete pipeline for VCF file analysis and visualization'
    )

    analysis_group = parser.add_argument_group('VCF Analysis')
    analysis_group.add_argument('vcf_file', nargs='?', help='VCF file to analyze')
    analysis_group.add_argument('max_variants', nargs='?', type=int, help='Max variants')
    analysis_group.add_argument('--output-dir', default='vcf_analysis_results',
                                help='Output directory')
    analysis_group.add_argument('--chunk-size', type=int, default=50000,
                                help='Chunk size')

    web_group = parser.add_argument_group('Web Dashboard')
    web_group.add_argument('--no-dashboard', action='store_true',
                           help='Do not launch dashboard')
    web_group.add_argument('--dashboard-only', action='store_true',
                           help='Launch dashboard only')
    web_group.add_argument('--web-only', action='store_true', help='Alias for dashboard-only')
    web_group.add_argument('--host', default='127.0.0.1', help='Host')
    web_group.add_argument('--port', type=int, default=5000, help='Port')
    web_group.add_argument('--no-browser', action='store_true',
                           help='Do not open browser')

    utility_group = parser.add_argument_group('Utilities')
    utility_group.add_argument('--list-analyses', action='store_true')
    utility_group.add_argument('--clean', action='store_true')

    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_arguments()

    print("\n" + "=" * 80)
    print("VCF PIPELINE - vcf-stats")
    print("=" * 80)

    pipeline = VCFPipeline()

    if args.list_analyses:
        list_available_analyses(args.output_dir)
        return

    if args.clean:
        clean_results_directory(args.output_dir)
        return

    if args.dashboard_only or args.web_only:
        pipeline.launch_web_dashboard(
            output_dir=args.output_dir,
            host=args.host,
            port=args.port,
            open_browser=not args.no_browser
        )
        return

    if not args.vcf_file:
        print("Error: VCF file required for analysis")
        print("Usage: vcf-analyze file.vcf [options]")
        return

    pipeline.run_complete_pipeline(
        vcf_file=args.vcf_file,
        max_variants=args.max_variants,
        output_dir=args.output_dir,
        chunk_size=args.chunk_size,
        launch_dashboard=not args.no_dashboard,
        dashboard_host=args.host,
        dashboard_port=args.port
    )


if __name__ == "__main__":
    main()