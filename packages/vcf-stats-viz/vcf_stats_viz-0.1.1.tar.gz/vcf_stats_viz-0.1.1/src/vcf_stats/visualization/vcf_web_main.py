import sys
import logging
import webbrowser
import threading
import time
import os
import argparse
from .vcf_web_dashboard import VCFWebDashboard
from .vcf_web_routes import setup_routes
from .vcf_web_templates import create_html_template, create_javascript_file
from .vcf_web_data import load_initial_data

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def initialize_dashboard(dashboard: VCFWebDashboard, open_browser: bool = True):
    """
    Initialize the web dashboard.

    Args:
        dashboard: Dashboard instance
        open_browser: If True, automatically opens browser
    """
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    static_dir = os.path.join(os.path.dirname(__file__), 'static')

    create_html_template(template_dir)
    create_javascript_file(static_dir)

    setup_routes(dashboard.get_app(), dashboard)

    load_initial_data(dashboard)

    if open_browser:
        def open_browser_delayed():
            time.sleep(1.5)
            webbrowser.open(f'http://{dashboard.host}:{dashboard.port}')

        threading.Thread(target=open_browser_delayed).start()

    logger.info(f"Web server started at http://{dashboard.host}:{dashboard.port}")
    logger.info("VCF Dashboard ready to use!")
    logger.info("Use Ctrl+C to stop the server")


def main():
    """Main function to run the web dashboard."""
    parser = argparse.ArgumentParser(description='Web Dashboard for VCF Visualization')
    parser.add_argument('--results-dir', default='vcf_analysis_results',
                        help='Directory with analysis results')
    parser.add_argument('--host', default='127.0.0.1', help='Web server host')
    parser.add_argument('--port', type=int, default=5000, help='Web server port')
    parser.add_argument('--no-browser', action='store_true',
                        help='Do not open browser automatically')
    parser.add_argument('--debug', action='store_true',
                        help='Debug mode')

    args = parser.parse_args()

    dashboard = VCFWebDashboard(
        results_dir=args.results_dir,
        host=args.host,
        port=args.port
    )

    initialize_dashboard(dashboard, open_browser=not args.no_browser)

    dashboard.run_server(debug=args.debug)


if __name__ == '__main__':
    main()