import os
import json
import pandas as pd
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


def load_initial_data(dashboard, analysis_id: str = None) -> bool:
    """
    Load initial data into the dashboard.
    """
    try:
        results_dir = dashboard.get_results_dir()

        if analysis_id is None:
            analyses = discover_analyses(results_dir)
            if analyses:
                analysis_id = analyses[0]['id']
                logger.info(f"Loading most recent analysis: {analysis_id}")
            else:
                logger.warning("No analyses available")
                return False

        return load_analysis_data(analysis_id, dashboard)

    except Exception as e:
        logger.error(f"Error loading initial data: {e}")
        return False


def discover_analyses(results_dir: str) -> List[Dict]:
    """
    Discover available analyses in the directory.
    """
    analyses = []

    if not os.path.exists(results_dir):
        logger.warning(f"Directory {results_dir} does not exist")
        return analyses

    try:
        metadata_files = [f for f in os.listdir(results_dir)
                          if f.startswith('metadata_') and f.endswith('.json')]

        summary_files = [f for f in os.listdir(results_dir)
                         if f.startswith('summary_') and f.endswith('.json')]

        files_to_check = metadata_files if metadata_files else summary_files

        logger.info(f"Found {len(files_to_check)} analysis files")

        for analysis_file in files_to_check:
            try:
                file_path = os.path.join(results_dir, analysis_file)

                if analysis_file.startswith('metadata_'):
                    timestamp = analysis_file.replace('metadata_', '').replace('.json', '')
                    with open(file_path, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)

                    analyses.append({
                        'id': timestamp,
                        'name': f"Analysis {timestamp}",
                        'total_variants': metadata.get('total_variants',
                                                       metadata.get('sample_variants', 0)),
                        'date': metadata.get('analysis_date', timestamp),
                        'processing_mode': metadata.get('processing_mode', 'streaming'),
                        'has_full_data': metadata.get('output_files', {}).get('dataframe_path') is not None
                    })

                elif analysis_file.startswith('summary_'):
                    timestamp = analysis_file.replace('summary_', '').replace('.json', '')
                    with open(file_path, 'r', encoding='utf-8') as f:
                        summary = json.load(f)

                    analyses.append({
                        'id': timestamp,
                        'name': f"Analysis {timestamp}",
                        'total_variants': summary.get('total_variants', 0),
                        'date': timestamp,
                        'processing_mode': 'legacy',
                        'has_full_data': True
                    })

            except Exception as e:
                logger.error(f"Error reading analysis {analysis_file}: {e}")
                continue

        analyses.sort(key=lambda x: x.get('date', ''), reverse=True)
        logger.info(f"Total analyses discovered: {len(analyses)}")

        return analyses

    except Exception as e:
        logger.error(f"Error discovering analyses: {e}")
        return analyses


def load_analysis_data(analysis_id: str, dashboard) -> bool:
    """
    Load data from a specific analysis.

    Note: With streaming, we only load SAMPLE, not complete data.
    """
    try:
        logger.info(f"Loading analysis: {analysis_id}")
        results_dir = dashboard.get_results_dir()
        current_results = {}

        metadata_file = f"metadata_{analysis_id}.json"
        metadata_path = os.path.join(results_dir, metadata_file)
        if os.path.exists(metadata_path):
            logger.info(f"Loading metadata: {metadata_file}")
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            current_results['metadata'] = metadata

            processing_mode = metadata.get('processing_mode', 'streaming')
            current_results['processing_mode'] = processing_mode
        else:
            current_results['processing_mode'] = 'legacy'

        summary_file = f"summary_{analysis_id}.json"
        summary_path = os.path.join(results_dir, summary_file)
        if os.path.exists(summary_path):
            logger.info(f"Loading summary: {summary_file}")
            with open(summary_path, 'r', encoding='utf-8') as f:
                current_results['summary'] = json.load(f)
        else:
            logger.error(f"Summary file not found: {summary_file}")
            return False

        charts_file = f"charts_data_{analysis_id}.json"
        charts_path = os.path.join(results_dir, charts_file)
        if os.path.exists(charts_path):
            logger.info(f"Loading charts data: {charts_file}")
            with open(charts_path, 'r', encoding='utf-8') as f:
                current_results['charts_data'] = json.load(f)
        else:
            logger.warning(f"Charts data not found, generating from summary")
            current_results['charts_data'] = generate_charts_from_summary(
                current_results['summary']
            )

        sample_file = f"sample_{analysis_id}.parquet"
        sample_path = os.path.join(results_dir, sample_file)

        variants_file = f"variants_{analysis_id}.parquet"
        variants_path = os.path.join(results_dir, variants_file)

        if os.path.exists(sample_path):
            logger.info(f"Loading SAMPLE: {sample_file}")
            current_results['dataframe'] = pd.read_parquet(sample_path)
            current_results['data_type'] = 'sample'
            logger.info(f"Sample loaded: {len(current_results['dataframe']):,} variants")

        elif os.path.exists(variants_path):
            logger.info(f"Loading COMPLETE data: {variants_file}")
            current_results['dataframe'] = pd.read_parquet(variants_path)
            current_results['data_type'] = 'full'
            logger.info(f"Complete DataFrame loaded: {len(current_results['dataframe']):,} variants")

        else:
            logger.warning("No tabular data found, using only statistics")
            current_results['dataframe'] = None
            current_results['data_type'] = 'stats_only'

        enrich_dashboard_data(current_results)

        dashboard.set_current_results(current_results)
        logger.info(f"Analysis {analysis_id} loaded successfully")
        logger.info(f"Mode: {current_results['processing_mode']}, Data type: {current_results['data_type']}")

        return True

    except Exception as e:
        logger.error(f"Error loading analysis {analysis_id}: {e}")
        return False


def generate_charts_from_summary(summary: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate chart data from summary.
    """
    charts_data = {}

    try:
        if 'chromosome_counts' in summary:
            chrom_data = summary['chromosome_counts']
            if isinstance(chrom_data, dict):
                charts_data['chromosome_distribution'] = {
                    'labels': list(chrom_data.keys()),
                    'values': list(chrom_data.values())
                }

        if 'variant_type_counts' in summary:
            type_data = summary['variant_type_counts']
            if isinstance(type_data, dict):
                charts_data['variant_types'] = {
                    'labels': list(type_data.keys()),
                    'values': list(type_data.values())
                }

        if 'filter_counts' in summary:
            filter_data = summary['filter_counts']
            if isinstance(filter_data, dict):
                charts_data['filter_distribution'] = {
                    'labels': list(filter_data.keys()),
                    'values': list(filter_data.values())
                }

        charts_data['summary_stats'] = {
            'total_variants': summary.get('total_variants', 0),
            'chromosomes_count': len(summary.get('chromosome_counts', {})),
            'variant_types_count': len(summary.get('variant_type_counts', {})),
            'quality_average': summary.get('quality_average', 0),
            'sample_size': summary.get('sample_size', 0)
        }

    except Exception as e:
        logger.error(f"Error generating charts from summary: {e}")

    return charts_data


def enrich_dashboard_data(results: Dict[str, Any]):
    """
    Enrich data for the web dashboard.
    """
    try:
        summary = results.get('summary', {})
        df = results.get('dataframe')

        results['dashboard_info'] = {
            'has_table_data': df is not None and len(df) > 0,
            'total_variants_estimated': summary.get('total_variants', 0),
            'sample_size_actual': len(df) if df is not None else 0,
            'processing_time': summary.get('processing_time_seconds', 0),
            'file_size_mb': summary.get('file_size_mb', 0)
        }

        if df is not None and not df.empty:
            if 'QUAL' in df.columns:
                qual_stats = {
                    'mean': float(df['QUAL'].mean()),
                    'median': float(df['QUAL'].median()),
                    'min': float(df['QUAL'].min()),
                    'max': float(df['QUAL'].max())
                }
                results['quality_stats'] = qual_stats

            info_fields = [col for col in df.columns
                           if col not in ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'VARIANT_TYPE']]
            results['info_fields'] = info_fields[:20]

    except Exception as e:
        logger.error(f"Error enriching dashboard data: {e}")