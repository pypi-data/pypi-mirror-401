import os
import json
import logging
from datetime import datetime
from typing import Dict, Set, Tuple, Any
import pandas as pd
from cyvcf2 import VCF

logger = logging.getLogger(__name__)


def detect_info_fields_and_size(file_path: str, sample_lines: int = 10000) -> Tuple[Set[str], Dict[str, Any]]:
    """
    Detect INFO fields and gather file metadata in a single pass.
    """
    info_fields = set()
    file_info = {}

    logger.info(f"Analyzing VCF file: {file_path}")

    try:
        file_size = os.path.getsize(file_path)
        file_info['file_size_mb'] = round(file_size / (1024 * 1024), 2)

        vcf_reader = VCF(file_path)
        variant_count = 0

        for variant in vcf_reader:
            if variant.INFO:
                info_dict = dict(variant.INFO)
                info_fields.update(info_dict.keys())

            variant_count += 1
            if variant_count >= sample_lines:
                break

        file_info['estimated_variants'] = variant_count
        vcf_reader.close()

        logger.info(f"INFO fields detected in {sample_lines} lines: {list(info_fields)}")
        logger.info(f"File size: {file_info['file_size_mb']} MB")
        logger.info(f"Estimated variants: {file_info['estimated_variants']:,}")

        return info_fields, file_info

    except Exception as e:
        logger.error(f"Error analyzing VCF file: {e}")
        return set(), {}


def save_analysis_results(df: pd.DataFrame, summary: Dict[str, Any],
                          output_dir: str = "vcf_analysis_results") -> Dict[str, str]:
    """
    Save analysis results for web usage and further analysis.
    Sorts data by position before saving (once).
    """
    from .vcf_parser import UniversalVCFParser

    try:
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        parser = UniversalVCFParser()

        logger.info(f"Optimizing DataFrame ({len(df):,} rows)...")
        df_optimized = df.copy()

        for col in df_optimized.select_dtypes(include=['int64']).columns:
            df_optimized[col] = pd.to_numeric(df_optimized[col], downcast='integer')
        for col in df_optimized.select_dtypes(include=['float64']).columns:
            df_optimized[col] = pd.to_numeric(df_optimized[col], downcast='float')

        for col in df_optimized.select_dtypes(include=['object']).columns:
            unique_count = df_optimized[col].nunique()
            if 0 < unique_count < min(1000, len(df_optimized) * 0.1):
                df_optimized[col] = df_optimized[col].astype('category')

        logger.info("Optimization completed")

        logger.info("Sorting DataFrame by CHROM and POS...")
        try:
            chrom_order = {}
            standard_order = [str(i) for i in range(1, 23)] + ['X', 'Y', 'M', 'MT']

            for chrom in df_optimized['CHROM'].unique():
                chrom_str = str(chrom)
                if chrom_str.startswith('chr'):
                    chrom_num = chrom_str[3:]
                else:
                    chrom_num = chrom_str

                if chrom_num in standard_order:
                    chrom_order[chrom_str] = standard_order.index(chrom_num)
                else:
                    chrom_order[chrom_str] = 999

            df_optimized['__chrom_sort'] = df_optimized['CHROM'].map(chrom_order)
            df_optimized = df_optimized.sort_values(['__chrom_sort', 'POS'])
            df_optimized = df_optimized.drop('__chrom_sort', axis=1)

            logger.info(f"DataFrame sorted ({len(df_optimized):,} rows)")
        except Exception as e:
            logger.warning(f"Could not sort completely: {e}")
            if 'CHROM' in df_optimized.columns and 'POS' in df_optimized.columns:
                df_optimized = df_optimized.sort_values(['CHROM', 'POS'])
                logger.info("DataFrame sorted (simple fallback)")

        df_path = os.path.join(output_dir, f"variants_{timestamp}.parquet")

        logger.info(f"Saving sorted DataFrame to {df_path}")

        if len(df_optimized) > 1000000:
            logger.info("Large dataset, using 'brotli' compression for better ratio")
            df_optimized.to_parquet(df_path, index=False, compression='brotli')
        else:
            df_optimized.to_parquet(df_path, index=False, compression='snappy')

        file_size_mb = os.path.getsize(df_path) / (1024 * 1024)
        logger.info(f"DataFrame saved: {df_path} ({file_size_mb:.1f} MB, {len(df_optimized):,} variants)")

        summary_path = os.path.join(output_dir, f"summary_{timestamp}.json")
        serializable_summary = parser._make_serializable(summary)

        serializable_summary['data_processing'] = {
            'sorted_by_position': True,
            'sorting_method': 'chromosome_and_position',
            'total_variants_saved': len(df_optimized)
        }

        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(serializable_summary, f, indent=2, ensure_ascii=False)
        logger.info(f"Summary saved: {summary_path}")

        charts_data = parser._prepare_charts_data(df_optimized, summary)
        charts_path = os.path.join(output_dir, f"charts_data_{timestamp}.json")
        with open(charts_path, 'w', encoding='utf-8') as f:
            json.dump(charts_data, f, indent=2, ensure_ascii=False)
        logger.info(f"Chart data saved: {charts_path}")

        metadata = {
            'timestamp': timestamp,
            'total_variants': len(df_optimized),
            'file_size_mb': round(file_size_mb, 2),
            'processing_mode': 'optimized_dask_with_sorting',
            'data_ordered': True,
            'output_files': {
                'dataframe': df_path,
                'summary': summary_path,
                'charts_data': charts_path
            },
            'analysis_date': datetime.now().isoformat(),
            'sorting_info': {
                'sorted_by': ['CHROM', 'POS'],
                'chromosome_order': 'standard (1-22, X, Y, M)'
            }
        }

        metadata_path = os.path.join(output_dir, f"metadata_{timestamp}.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        logger.info(f"All results saved in: {output_dir}")

        return {
            'dataframe_path': df_path,
            'summary_path': summary_path,
            'charts_data_path': charts_path,
            'metadata_path': metadata_path,
            'output_dir': output_dir
        }

    except Exception as e:
        logger.error(f"Error saving results: {e}")
        import traceback
        traceback.print_exc()
        return {}