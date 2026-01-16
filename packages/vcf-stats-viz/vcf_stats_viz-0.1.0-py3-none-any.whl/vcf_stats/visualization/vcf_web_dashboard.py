from flask import Flask
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class VCFWebDashboard:
    """Servidor web para visualizar resultados del análisis VCF."""

    def __init__(self, results_dir: str = "vcf_analysis_results",
                 host: str = "127.0.0.1", port: int = 5000):
        self.results_dir = results_dir
        self.host = host
        self.port = port
        self.current_results: Dict[str, Any] = {}

        self.app = Flask(__name__,
                         static_folder='static',
                         template_folder='templates')

    def get_app(self):
        """Obtener la aplicación Flask."""
        return self.app

    def get_current_results(self):
        """Obtener resultados actuales cargados."""
        return self.current_results

    def set_current_results(self, results: Dict[str, Any]):
        """Establecer resultados actuales."""
        self.current_results = results

    def get_results_dir(self):
        """Obtener directorio de resultados."""
        return self.results_dir

    def run_server(self, debug: bool = False):
        """Ejecutar el servidor web."""
        logger.info(f"🌐 Servidor web iniciado en http://{self.host}:{self.port}")
        self.app.run(host=self.host, port=self.port, debug=debug)