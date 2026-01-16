import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Set, Tuple, Iterator, Any, Union
import logging
from cyvcf2 import VCF

logger = logging.getLogger(__name__)


class UniversalVCFParser:
    """
    Universal VCF parser optimized using cyvcf2 for high-performance processing.
    """
    VALID_CHROMOSOMES = [f'chr{i}' for i in list(range(1, 23)) + ['X', 'Y', 'M']] + \
                        [str(i) for i in list(range(1, 23)) + ['X', 'Y', 'M']]

    def infer_variant_type(self, ref: str, alt: str) -> str:
        """
        Infer the type of genetic variant based on REF and ALT alleles.
        """
        if ref == '.' or alt == '.' or not ref or not alt:
            return 'UNKNOWN'

        if alt.startswith('<') or ref.startswith('<'):
            return 'STRUCTURAL'

        alt_alleles = alt.split(',')
        if len(alt_alleles) > 1:
            return 'MULTIALLELIC'

        alt_allele = alt_alleles[0]

        if len(ref) == len(alt_allele):
            if len(ref) == 1:
                return 'SNP'
            else:
                return 'MNP'
        elif len(ref) > len(alt_allele):
            return 'DELETION'
        elif len(ref) < len(alt_allele):
            return 'INSERTION'
        else:
            return 'INDEL'

    def parse_info_dict(self, info_dict: Dict) -> Dict[str, Any]:
        """
        Parse cyvcf2 INFO dictionary to standard Python types.
        """
        parsed_info = {}

        for key, value in info_dict.items():
            if value is None:
                parsed_info[key] = True
            elif isinstance(value, (list, tuple)):
                if len(value) == 1:
                    parsed_info[key] = self._convert_value(value[0])
                else:
                    parsed_info[key] = [self._convert_value(v) for v in value]
            else:
                parsed_info[key] = self._convert_value(value)

        return parsed_info

    def _convert_value(self, value: Any) -> Any:
        """
        Convert individual values to appropriate Python types.
        """
        if value is None:
            return True
        elif isinstance(value, (int, float, bool)):
            return value
        elif isinstance(value, str):
            if value.replace('.', '').replace('-', '').isdigit():
                if '.' in value:
                    try:
                        return float(value)
                    except ValueError:
                        return value
                else:
                    try:
                        return int(value)
                    except ValueError:
                        return value
            elif value.lower() in ['true', 'false']:
                return value.lower() == 'true'
            else:
                return value
        else:
            return str(value)

    def parse_vcf_lazy(self, file_path: str, max_variants: Optional[int] = None) -> Iterator[Dict[str, Any]]:
        """
        Lazy VCF parsing that returns an iterator for memory-efficient processing.
        """
        try:
            vcf_reader = VCF(file_path)
            variant_count = 0

            for variant in vcf_reader:
                record = {
                    'CHROM': variant.CHROM,
                    'POS': variant.POS,
                    'ID': variant.ID if variant.ID else '.',
                    'REF': variant.REF,
                    'ALT': ','.join(variant.ALT) if variant.ALT else '.',
                    'QUAL': variant.QUAL if variant.QUAL else 0.0,
                    'FILTER': variant.FILTER if variant.FILTER else 'PASS',
                    'VARIANT_TYPE': self.infer_variant_type(variant.REF, ','.join(variant.ALT) if variant.ALT else '.')
                }

                if variant.INFO:
                    info_dict = self.parse_info_dict(dict(variant.INFO))
                    record.update(info_dict)

                yield record
                variant_count += 1

                if max_variants and variant_count >= max_variants:
                    logger.info(f"Limit reached in lazy mode: {max_variants:,} variants")
                    break

            vcf_reader.close()

        except Exception as e:
            logger.error(f"Error in lazy processing: {e}")

    def get_comprehensive_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate comprehensive summary statistics for the variant dataset.
        """
        if df.empty:
            return {}

        summary = {
            'total_variants': len(df),
            'chromosome_counts': df['CHROM'].value_counts().to_dict(),
            'variant_type_counts': df['VARIANT_TYPE'].value_counts().to_dict(),
            'quality_stats': {
                'mean': float(df['QUAL'].mean()),
                'median': float(df['QUAL'].median()),
                'std': float(df['QUAL'].std()),
                'min': float(df['QUAL'].min()),
                'max': float(df['QUAL'].max())
            } if 'QUAL' in df.columns and df['QUAL'].notna().any() else {},
            'filter_counts': df['FILTER'].value_counts().to_dict() if 'FILTER' in df.columns else {},
            'columns_available': list(df.columns),
            'missing_data_percentage': (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
            'memory_usage_mb': round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)
        }

        info_columns = [col for col in df.columns if col not in
                        ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'VARIANT_TYPE']]

        summary['info_fields_detected'] = info_columns

        for col in info_columns:
            non_null_count = df[col].notna().sum()
            unique_count = df[col].nunique()

            summary[f'{col}_info'] = {
                'non_null_count': non_null_count,
                'non_null_percentage': round((non_null_count / len(df)) * 100, 2),
                'unique_values': unique_count
            }

            if pd.api.types.is_numeric_dtype(df[col]):
                summary[f'{col}_info'].update({
                    'mean': float(df[col].mean()),
                    'median': float(df[col].median()),
                    'min': float(df[col].min()),
                    'max': float(df[col].max())
                })
            elif unique_count <= 20:
                summary[f'{col}_info']['top_values'] = df[col].value_counts().head(10).to_dict()

        return summary

    def _make_serializable(self, obj: Any) -> Any:
        """
        Convert objects to JSON-serializable types.
        """
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {k: self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._make_serializable(item) for item in obj]
        elif pd.isna(obj):
            return None
        else:
            return obj

    def _prepare_charts_data(self, df: pd.DataFrame, summary: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare specific data for web charts and visualizations.
        """
        charts_data = {}

        try:
            chrom_data = df['CHROM'].value_counts().head(20)
            charts_data['chromosome_distribution'] = {
                'labels': chrom_data.index.tolist(),
                'values': chrom_data.values.tolist()
            }

            variant_type_data = df['VARIANT_TYPE'].value_counts()
            charts_data['variant_types'] = {
                'labels': variant_type_data.index.tolist(),
                'values': variant_type_data.values.tolist()
            }

            if 'QUAL' in df.columns and df['QUAL'].notna().any():
                qual_data = df['QUAL'].dropna()
                charts_data['quality_distribution'] = {
                    'bins': np.histogram(qual_data, bins=50)[0].tolist(),
                    'range': [float(qual_data.min()), float(qual_data.max())]
                }

            info_fields_usage = {}
            info_columns = [col for col in df.columns if col not in
                            ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'VARIANT_TYPE']]

            for col in info_columns[:10]:
                non_null_count = df[col].notna().sum()
                info_fields_usage[col] = {
                    'non_null': int(non_null_count),
                    'total': len(df),
                    'percentage': round((non_null_count / len(df)) * 100, 2)
                }

            charts_data['info_fields_usage'] = info_fields_usage

            charts_data['summary_stats'] = {
                'total_variants': len(df),
                'chromosomes_count': df['CHROM'].nunique(),
                'variant_types_count': df['VARIANT_TYPE'].nunique(),
                'memory_usage_mb': summary.get('memory_usage_mb', 0)
            }

        except Exception as e:
            logger.error(f"Error preparing chart data: {e}")

        return charts_data