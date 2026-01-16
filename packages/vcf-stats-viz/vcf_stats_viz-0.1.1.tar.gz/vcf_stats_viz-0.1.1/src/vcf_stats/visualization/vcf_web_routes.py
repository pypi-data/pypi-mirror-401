from flask import jsonify, request, send_from_directory, render_template
import pandas as pd
import numpy as np
import json
import os
from typing import Dict, Any
import logging
from .vcf_web_data import discover_analyses, load_analysis_data
logger = logging.getLogger(__name__)


def setup_routes(app, dashboard):
    """Configure all web server routes."""

    @app.route('/')
    def index():
        """Main dashboard page."""
        return render_template('index.html')

    @app.route('/static/<path:filename>')
    def serve_static(filename):
        """Serve static files."""
        return send_from_directory(app.static_folder, filename)

    @app.route('/api/data/summary')
    def get_summary():
        """API: Get general summary."""
        current_results = dashboard.get_current_results()
        summary = current_results.get('summary', {})

        summary['processing_mode'] = current_results.get('processing_mode', 'unknown')
        summary['data_type'] = current_results.get('data_type', 'unknown')
        summary['dashboard_info'] = current_results.get('dashboard_info', {})

        return jsonify(summary)

    @app.route('/api/data/charts')
    def get_charts_data():
        """API: Get data for charts."""
        current_results = dashboard.get_current_results()
        return jsonify(current_results.get('charts_data', {}))

    @app.route('/api/data/metadata')
    def get_metadata():
        """API: Get metadata."""
        current_results = dashboard.get_current_results()
        return jsonify(current_results.get('metadata', {}))

    @app.route('/api/data/variants')
    def get_variants():
        """API: Get variants (paginated) SORTED by position."""
        try:
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 50))
            sort_by = request.args.get('sort_by', 'position')

            current_results = dashboard.get_current_results()
            df = current_results.get('dataframe')
            processing_mode = current_results.get('processing_mode', 'streaming')

            if df is not None and len(df) > 0:
                start_idx = (page - 1) * per_page
                end_idx = start_idx + per_page

                if 'CHROM' in df.columns and 'POS' in df.columns:
                    temp_df = df.copy()

                    chrom_order = {}
                    unique_chroms = temp_df['CHROM'].unique()

                    standard_order = [str(i) for i in range(1, 23)] + ['X', 'Y', 'M', 'MT']

                    for chrom in unique_chroms:
                        chrom_str = str(chrom)
                        if chrom_str.startswith('chr'):
                            chrom_num = chrom_str[3:]
                        else:
                            chrom_num = chrom_str

                        if chrom_num in standard_order:
                            chrom_order[chrom_str] = standard_order.index(chrom_num)
                        else:
                            chrom_order[chrom_str] = 999

                    temp_df['__chrom_sort'] = temp_df['CHROM'].map(chrom_order)
                    temp_df = temp_df.sort_values(['__chrom_sort', 'POS'])

                    variants_page = temp_df.iloc[start_idx:end_idx]
                    variants_page = variants_page.drop('__chrom_sort', axis=1, errors='ignore')
                else:
                    variants_page = df.iloc[start_idx:end_idx]

                response = {
                    'page': page,
                    'per_page': per_page,
                    'variants': variants_page.replace({np.nan: None}).to_dict('records'),
                    'processing_mode': processing_mode,
                    'data_type': current_results.get('data_type', 'unknown'),
                    'sorted_by': 'position' if 'CHROM' in df.columns and 'POS' in df.columns else 'original'
                }

                if processing_mode == 'streaming':
                    total_estimated = current_results.get('summary', {}).get('total_variants', 0)
                    sample_size = len(df)
                    response.update({
                        'total_variants_estimated': total_estimated,
                        'sample_size': sample_size,
                        'is_sample': True,
                        'note': f'Showing {sample_size:,} sample variants'
                    })
                else:
                    response.update({
                        'total_variants': len(df),
                        'total_pages': (len(df) + per_page - 1) // per_page,
                        'is_sample': False
                    })

                return jsonify(response)
            else:
                return jsonify({
                    'error': 'No tabular data available',
                    'processing_mode': processing_mode,
                    'has_table_data': False
                })

        except Exception as e:
            logger.error(f"Error getting variants: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/data/chromosome/<chrom>')
    def get_chromosome_data(chrom):
        """API: Get specific chromosome data."""
        try:
            current_results = dashboard.get_current_results()
            df = current_results.get('dataframe')

            if df is not None and len(df) > 0:
                chrom_data = df[df['CHROM'] == chrom]

                if len(chrom_data) > 0:
                    return jsonify({
                        'chromosome': chrom,
                        'variants_in_sample': len(chrom_data),
                        'variant_types': chrom_data['VARIANT_TYPE'].value_counts().to_dict(),
                        'quality_stats': {
                            'mean': float(chrom_data['QUAL'].mean()) if 'QUAL' in chrom_data.columns else 0,
                            'min': float(chrom_data['QUAL'].min()) if 'QUAL' in chrom_data.columns else 0,
                            'max': float(chrom_data['QUAL'].max()) if 'QUAL' in chrom_data.columns else 0
                        },
                        'is_sample_data': current_results.get('processing_mode') == 'streaming'
                    })
                else:
                    summary = current_results.get('summary', {})
                    chrom_counts = summary.get('chromosome_counts', {})
                    return jsonify({
                        'chromosome': chrom,
                        'variants_estimated': chrom_counts.get(chrom, 0),
                        'note': 'Estimated data from statistics (sample does not contain this chromosome)'
                    })
            else:
                summary = current_results.get('summary', {})
                chrom_counts = summary.get('chromosome_counts', {})
                return jsonify({
                    'chromosome': chrom,
                    'variants_estimated': chrom_counts.get(chrom, 0),
                    'note': 'Estimated data from statistics'
                })

        except Exception as e:
            logger.error(f"Error getting chromosome {chrom} data: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/data/search')
    def search_variants():
        """API: Search variants (only in available sample)."""
        try:
            query = request.args.get('q', '').strip()
            if not query:
                return jsonify({'error': 'Empty query'}), 400

            current_results = dashboard.get_current_results()
            df = current_results.get('dataframe')
            processing_mode = current_results.get('processing_mode', 'streaming')

            if df is not None and len(df) > 0:
                # Primero: intentar búsqueda numérica para POS (más eficiente)
                results = None

                if 'POS' in df.columns:
                    try:
                        query_int = int(query)
                        results = df[df['POS'] == query_int]
                    except ValueError:
                        # No es un número, continuar con búsqueda de texto
                        pass

                # Si no se encontró por POS o no era número, buscar en otras columnas
                if results is None or len(results) == 0:
                    # Columnas para búsqueda (excluimos POS que ya se procesó)
                    search_columns = ['CHROM', 'ID', 'REF', 'ALT', 'VARIANT_TYPE', 'GENE']

                    # Filtrar columnas que existen
                    existing_columns = [col for col in search_columns if col in df.columns]

                    if not existing_columns:
                        results = pd.DataFrame()
                    else:
                        # Usar numpy para búsqueda exacta eficiente
                        mask = np.zeros(len(df), dtype=bool)

                        for col in existing_columns:
                            # Para búsqueda exacta: comparar directamente
                            col_values = df[col].values

                            # Manejar NaN y tipos
                            if pd.api.types.is_string_dtype(df[col]):
                                # Para strings: búsqueda exacta
                                col_mask = col_values == query
                            else:
                                # Para otros tipos: convertir a string y comparar
                                col_mask = np.array([str(x) == query if pd.notna(x) else False
                                                     for x in col_values])

                            mask = mask | col_mask

                        results = df[mask]

                # Limitar resultados
                results = results.head(100) if not results.empty else results

                response = {
                    'query': query,
                    'results_found_in_sample': len(results),
                    'processing_mode': processing_mode
                }

                if not results.empty:
                    response['results'] = results.replace({np.nan: None}).to_dict('records')
                    response['total_found'] = len(results)
                else:
                    response['results'] = []
                    response['total_found'] = 0

                if processing_mode == 'streaming':
                    response['note'] = 'Search performed on data sample (exact match)'
                else:
                    response['note'] = 'Search in complete data (exact match)'

                return jsonify(response)
            else:
                return jsonify({
                    'error': 'No tabular data available for search',
                    'processing_mode': processing_mode,
                    'note': 'This analysis only contains statistics'
                })

        except Exception as e:
            logger.error(f"Error searching variants: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/files')
    def get_available_files():
        """API: Get list of available analyses."""
        try:
            analyses = discover_analyses(dashboard.get_results_dir())

            for analysis in analyses:
                analysis['display_name'] = (
                    f"{analysis['name']} - "
                    f"{analysis['total_variants']:,} vars - "
                    f"{analysis.get('processing_mode', 'unknown')}"
                )

            return jsonify({'analyses': analyses})
        except Exception as e:
            logger.error(f"Error getting available files: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/load/<analysis_id>')
    def load_analysis(analysis_id):
        """API: Load a specific analysis."""
        try:
            success = load_analysis_data(analysis_id, dashboard)
            if success:
                return jsonify({
                    'status': 'success',
                    'message': 'Analysis loaded successfully',
                    'analysis_id': analysis_id
                })
            else:
                return jsonify({'error': 'Could not load analysis'}), 404
        except Exception as e:
            logger.error(f"Error loading analysis {analysis_id}: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/system/info')
    def get_system_info():
        """API: Get system and configuration information."""
        try:
            current_results = dashboard.get_current_results()

            info = {
                'results_dir': dashboard.get_results_dir(),
                'processing_mode': current_results.get('processing_mode', 'unknown'),
                'data_type': current_results.get('data_type', 'unknown'),
                'has_table_data': current_results.get('dataframe') is not None,
                'table_size': len(current_results.get('dataframe'))
                if current_results.get('dataframe') is not None else 0
            }

            return jsonify(info)
        except Exception as e:
            logger.error(f"Error getting system information: {e}")
            return jsonify({'error': str(e)}), 500