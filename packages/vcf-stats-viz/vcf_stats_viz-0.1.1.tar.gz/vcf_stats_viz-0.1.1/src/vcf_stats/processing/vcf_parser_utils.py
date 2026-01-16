import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Iterator, List
import logging
import gc
from cyvcf2 import VCF
from .vcf_parser import UniversalVCFParser
import dask.dataframe as dd
from dask.diagnostics import ProgressBar
import tempfile
import os

logger = logging.getLogger(__name__)


def parse_vcf_lazy(file_path: str, max_variants: Optional[int] = None) -> Iterator[Dict[str, Any]]:
    """
    Lazy VCF parsing for memory-efficient processing.
    """
    parser = UniversalVCFParser()
    return parser.parse_vcf_lazy(file_path, max_variants)


def parse_vcf_complete_optimized(file_path: str, max_variants: Optional[int] = None,
                                 chunk_size: int = 50000, optimize_memory: bool = True) -> pd.DataFrame:
    """
    Simplified version: Uses Dask for fast processing, data is sorted when saving.
    """
    logger.info(f"Starting optimized load (chunk_size={chunk_size:,})")

    if max_variants and max_variants <= 100000:
        logger.info("Small file, using simple method...")
        return _parse_simple(file_path, max_variants)

    return _parse_with_dask_fast(file_path, max_variants, chunk_size)


def _parse_with_dask_fast(file_path: str, max_variants: Optional[int],
                          chunk_size: int) -> pd.DataFrame:
    """
    Process with Dask fast WITHOUT worrying about order.
    Data will be sorted later when saving.
    """
    parser = UniversalVCFParser()
    temp_dir = tempfile.mkdtemp(prefix="vcf_dask_fast_")

    try:
        logger.info(f"Processing with Dask (chunk_size={chunk_size:,})...")
        start_time = pd.Timestamp.now()

        chunk_files = []
        current_chunk = []
        total_processed = 0
        chunk_count = 0

        for record in parser.parse_vcf_lazy(file_path, max_variants):
            current_chunk.append(record)
            total_processed += 1

            if len(current_chunk) >= chunk_size:
                chunk_df = pd.DataFrame(current_chunk)
                chunk_df = _optimize_dataframe_memory(chunk_df)

                chunk_file = os.path.join(temp_dir, f"chunk_{chunk_count}.parquet")
                chunk_df.to_parquet(chunk_file, index=False, compression='snappy')
                chunk_files.append(chunk_file)

                current_chunk = []
                chunk_count += 1
                gc.collect()

                if chunk_count % 10 == 0:
                    elapsed = (pd.Timestamp.now() - start_time).total_seconds()
                    import psutil
                    memory_mb = psutil.Process().memory_info().rss / (1024 * 1024)
                    logger.info(f"Chunk {chunk_count}: {total_processed:,} var, {memory_mb:.1f} MB")

                if max_variants and total_processed >= max_variants:
                    break

        if current_chunk:
            chunk_df = pd.DataFrame(current_chunk)
            chunk_df = _optimize_dataframe_memory(chunk_df)
            chunk_file = os.path.join(temp_dir, f"chunk_{chunk_count}.parquet")
            chunk_df.to_parquet(chunk_file, index=False, compression='snappy')
            chunk_files.append(chunk_file)
            chunk_count += 1

        logger.info(f"Processed {chunk_count} chunks, total: {total_processed:,} variants")

        if chunk_files:
            logger.info("Concatenating chunks with Dask...")

            dask_df = dd.read_parquet(chunk_files)

            logger.info("Computing final DataFrame...")
            final_df = dask_df.compute()

            elapsed = (pd.Timestamp.now() - start_time).total_seconds()
            logger.info(f"Dask processing completed: {len(final_df):,} variants in {elapsed:.1f}s")
            logger.info(f"NOTE: Unsorted data - will be sorted when saving")

            return final_df

    except Exception as e:
        logger.error(f"Error in Dask processing: {e}")
        logger.info("Fallback to simple method...")
        return _parse_simple(file_path, max_variants)
    finally:
        if os.path.exists(temp_dir):
            for f in os.listdir(temp_dir):
                try:
                    os.remove(os.path.join(temp_dir, f))
                except:
                    pass
            try:
                os.rmdir(temp_dir)
            except:
                pass

    return pd.DataFrame()


def _parse_simple(file_path: str, max_variants: Optional[int]) -> pd.DataFrame:
    """
    Simple load for small files or testing.
    """
    parser = UniversalVCFParser()
    data = []
    variant_count = 0

    logger.info("Loading VCF with simple method...")

    start_time = pd.Timestamp.now()

    for record in parser.parse_vcf_lazy(file_path, max_variants):
        data.append(record)
        variant_count += 1

        if variant_count % 100000 == 0:
            elapsed = (pd.Timestamp.now() - start_time).total_seconds()
            logger.info(f"Loaded {variant_count:,} variants... ({elapsed:.1f}s)")

    if data:
        df = pd.DataFrame(data)
        df = _optimize_dataframe_memory(df)

        elapsed_total = (pd.Timestamp.now() - start_time).total_seconds()
        logger.info(f"Simple DataFrame: {len(df):,} rows in {elapsed_total:.1f}s")

        return df
    else:
        return pd.DataFrame()


def _optimize_dataframe_memory(df: pd.DataFrame, force_categorical_int8: bool = True) -> pd.DataFrame:
    """
    Optimize DataFrame data types to save memory.
    """
    try:
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str)

        for col in df.select_dtypes(include=['int64']).columns:
            if df[col].notna().any():
                min_val = df[col].min()
                max_val = df[col].max()
                if min_val >= -128 and max_val <= 127:
                    df[col] = pd.to_numeric(df[col], downcast='integer')
                elif min_val >= -32768 and max_val <= 32767:
                    df[col] = df[col].astype('int16')
                elif min_val >= -2147483648 and max_val <= 2147483647:
                    df[col] = df[col].astype('int32')
                else:
                    df[col] = pd.to_numeric(df[col], downcast='integer')

        for col in df.select_dtypes(include=['float64']).columns:
            df[col] = pd.to_numeric(df[col], downcast='float')

        for col in df.select_dtypes(include=['object']).columns:
            unique_count = df[col].nunique()
            total_count = len(df)

            if 0 < unique_count < min(1000, total_count * 0.3):
                df[col] = df[col].astype('category')

        type_guarantees = {
            'CHROM': 'category',
            'POS': 'int32',
            'ID': 'category',
            'REF': 'category',
            'ALT': 'category',
            'QUAL': 'float32',
            'FILTER': 'category',
            'VARIANT_TYPE': 'category'
        }

        for col, dtype in type_guarantees.items():
            if col in df.columns:
                try:
                    df[col] = df[col].astype(dtype)
                except Exception:
                    pass

        logger.debug(f"Optimized DataFrame: {df.memory_usage().sum() / (1024 * 1024):.1f} MB")
        return df

    except Exception as e:
        logger.warning(f"Error optimizing DataFrame: {e}")
        return df


def read_vcf_direct_traditional(file_path: str, max_variants: Optional[int] = None) -> pd.DataFrame:
    """
    [BENCHMARKING] Traditional direct reading for comparison.
    """
    logger.info(f"[BENCHMARK] Traditional reading: {file_path}")

    data = []
    variant_count = 0

    try:
        vcf_reader = VCF(file_path)
        start_time = pd.Timestamp.now()

        for variant in vcf_reader:
            record = {
                'CHROM': variant.CHROM,
                'POS': variant.POS,
                'ID': variant.ID if variant.ID else '.',
                'REF': variant.REF,
                'ALT': ','.join(variant.ALT) if variant.ALT else '.',
                'QUAL': variant.QUAL if variant.QUAL else 0.0,
                'FILTER': variant.FILTER if variant.FILTER else 'PASS',
            }

            if variant.INFO:
                for key, value in dict(variant.INFO).items():
                    if value is None:
                        record[key] = True
                    elif isinstance(value, (list, tuple)):
                        if len(value) == 1:
                            record[key] = value[0]
                        else:
                            record[key] = list(value)
                    else:
                        record[key] = value

            data.append(record)
            variant_count += 1

            if variant_count % 100000 == 0:
                elapsed = (pd.Timestamp.now() - start_time).total_seconds()
                logger.debug(f"[BENCHMARK] {variant_count:,} variants... ({elapsed:.1f}s)")

            if max_variants and variant_count >= max_variants:
                break

        vcf_reader.close()

        df = pd.DataFrame(data) if data else pd.DataFrame()

        elapsed_total = (pd.Timestamp.now() - start_time).total_seconds()
        logger.info(f"[BENCHMARK] Traditional: {len(df):,} rows in {elapsed_total:.1f}s")

        return df

    except Exception as e:
        logger.error(f"[BENCHMARK] Traditional error: {e}")
        return pd.DataFrame()


def parse_vcf_complete(file_path: str, max_variants: Optional[int] = None) -> pd.DataFrame:
    """
    Legacy function that now uses the optimized method.
    """
    return parse_vcf_complete_optimized(file_path, max_variants, chunk_size=50000)


def process_large_vcf_with_dask(file_path: str, max_variants: Optional[int] = None,
                                chunk_size: int = 50000, output_path: Optional[str] = None) -> dd.DataFrame:
    """
    Process very large VCFs using Dask.
    """
    logger.info(f"Starting processing with Dask (chunk_size={chunk_size:,})")

    df = _parse_with_dask_fast(file_path, max_variants, chunk_size)

    dask_df = dd.from_pandas(df, npartitions=max(1, len(df) // 50000))

    logger.info(f"Dask DataFrame created: {dask_df.npartitions} partitions")

    if output_path:
        logger.info(f"Saving result to {output_path}")
        with ProgressBar():
            dask_df.to_parquet(output_path, write_index=False, compression='snappy')
        logger.info(f"Result saved: {output_path}")

    return dask_df