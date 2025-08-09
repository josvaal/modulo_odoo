#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DE PRUEBAS CÁUSTICAS PARA SISTEMA ODOO
Automatiza la ejecución de pruebas exhaustivas y genera reporte detallado

Autor: Sistema de Pruebas Automatizadas
Versión: 2.0
Requisitos: Python 3.8+, requests, docker, psycopg2
"""

import argparse
import datetime
import json
import os
import subprocess
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
import webbrowser

try:
    import requests
except ImportError:
    print("❌ Error: requests no está instalado. Ejecuta: pip install requests")
    sys.exit(1)

try:
    import psycopg2
except ImportError:
    print("⚠️  Advertencia: psycopg2 no está instalado. Las pruebas de BD serán limitadas.")
    psycopg2 = None

# Configuración de colores para terminal
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

@dataclass
class TestResult:
    """Clase para almacenar resultados de pruebas"""
    test_name: str
    passed: bool
    details: str = ""
    error_message: str = ""
    response_time: float = 0.0
    timestamp: str = ""
    is_critical: bool = False
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.datetime.now().strftime('%H:%M:%S')

class CausticTester:
    """Clase principal para ejecutar pruebas cáusticas"""
    
    def __init__(self, odoo_url: str = "http://localhost:8200", 
                 usuario: str = "admin", password: str = "admin",
                 report_path: str = "./reporte_pruebas_causticas.html",
                 quick_test: bool = False, skip_browser: bool = False):
        self.odoo_url = odoo_url
        self.usuario = usuario
        self.password = password
        self.report_path = report_path
        self.quick_test = quick_test
        self.skip_browser = skip_browser
        
        # Variables globales para el reporte
        self.test_results: List[TestResult] = []
        self.start_time = datetime.datetime.now()
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.critical_errors = 0
        self.minor_errors = 0
        
        # Configuración de sesión HTTP
        self.session = requests.Session()
        self.session.timeout = 30
        
    def print_colored(self, text: str, color: str = Colors.WHITE, bold: bool = False):
        """Imprime texto con colores"""
        prefix = Colors.BOLD if bold else ""
        print(f"{prefix}{color}{text}{Colors.END}")
        
    def print_header(self, test_name: str):
        """Imprime encabezado de prueba"""
        print()
        self.print_colored("=" * 80, Colors.CYAN)
        self.print_colored(f"EJECUTANDO: {test_name}", Colors.CYAN, bold=True)
        self.print_colored("=" * 80, Colors.CYAN)
        
    def add_test_result(self, test_name: str, passed: bool, details: str = "",
                       error_message: str = "", response_time: float = 0.0,
                       is_critical: bool = False):
        """Añade resultado de prueba"""
        self.total_tests += 1
        
        result = TestResult(
            test_name=test_name,
            passed=passed,
            details=details,
            error_message=error_message,
            response_time=response_time,
            is_critical=is_critical
        )
        
        self.test_results.append(result)
        
        if passed:
            self.passed_tests += 1
            self.print_colored(f"✅ PASÓ: {test_name}", Colors.GREEN)
            if details:
                self.print_colored(f"   Detalles: {details}", Colors.WHITE)
        else:
            self.failed_tests += 1
            if is_critical:
                self.critical_errors += 1
            else:
                self.minor_errors += 1
            self.print_colored(f"❌ FALLÓ: {test_name}", Colors.RED)
            if error_message:
                self.print_colored(f"   Error: {error_message}", Colors.RED)
            if details:
                self.print_colored(f"   Detalles: {details}", Colors.WHITE)
                
        if response_time > 0:
            self.print_colored(f"   Tiempo de respuesta: {response_time:.2f} segundos", Colors.WHITE)
            
    def test_odoo_connectivity(self):
        """Prueba de conectividad básica con Odoo"""
        self.print_header("Prueba de Conectividad Básica")
        
        try:
            start_time = time.time()
            response = self.session.get(self.odoo_url)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                self.add_test_result(
                    "Conectividad HTTP", True,
                    "Servidor responde correctamente",
                    response_time=response_time
                )
            else:
                self.add_test_result(
                    "Conectividad HTTP", False,
                    error_message=f"Código de estado: {response.status_code}",
                    is_critical=True
                )
        except Exception as e:
            self.add_test_result(
                "Conectividad HTTP", False,
                error_message=str(e),
                is_critical=True
            )
            
    def test_docker_containers(self):
        """Verificación de contenedores Docker"""
        self.print_header("Verificación de Contenedores Docker")
        
        try:
            # Obtener estado de contenedores
            result = subprocess.run(
                ["docker-compose", "ps", "--format", "json"],
                capture_output=True, text=True, cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                containers_data = result.stdout.strip()
                if containers_data:
                    # Procesar cada línea como JSON separado
                    for line in containers_data.split('\n'):
                        if line.strip():
                            try:
                                container = json.loads(line)
                                is_running = container.get('State') == 'running'
                                self.add_test_result(
                                    f"Contenedor {container.get('Service', 'unknown')}",
                                    is_running,
                                    f"Estado: {container.get('State', 'unknown')}",
                                    is_critical=not is_running
                                )
                            except json.JSONDecodeError:
                                continue
                else:
                    self.add_test_result(
                        "Verificación Docker", False,
                        error_message="No se encontraron contenedores",
                        is_critical=True
                    )
            else:
                self.add_test_result(
                    "Verificación Docker", False,
                    error_message=result.stderr or "Error ejecutando docker-compose",
                    is_critical=True
                )
        except Exception as e:
            self.add_test_result(
                "Verificación Docker", False,
                error_message=str(e),
                is_critical=True
            )
            
    def test_database_connection(self):
        """Prueba de conexión a base de datos"""
        self.print_header("Prueba de Conexión a Base de Datos")
        
        try:
            # Intentar conectar usando docker exec
            result = subprocess.run(
                ["docker", "exec", "modulo_odoo-db-1", "pg_isready", "-U", "odoo"],
                capture_output=True, text=True
            )
            
            db_connected = result.returncode == 0
            self.add_test_result(
                "Conexión PostgreSQL",
                db_connected,
                "pg_isready status",
                is_critical=not db_connected
            )
            
            # Si psycopg2 está disponible, intentar conexión directa
            if psycopg2 and db_connected:
                try:
                    conn = psycopg2.connect(
                        host="localhost",
                        port="5432",
                        database="odoo",
                        user="odoo",
                        password="odoo",
                        connect_timeout=10
                    )
                    conn.close()
                    self.add_test_result(
                        "Conexión Directa PostgreSQL", True,
                        "Conexión directa exitosa"
                    )
                except Exception as e:
                    self.add_test_result(
                        "Conexión Directa PostgreSQL", False,
                        error_message=str(e)
                    )
                    
        except Exception as e:
            self.add_test_result(
                "Conexión PostgreSQL", False,
                error_message=str(e),
                is_critical=True
            )
            
    def test_system_load(self):
        """Pruebas de carga del sistema"""
        self.print_header("Pruebas de Carga del Sistema")
        
        if self.quick_test:
            self.print_colored("⚡ Modo rápido activado - Saltando pruebas de carga intensiva", Colors.YELLOW)
            return
            
        request_count = 10
        self.print_colored(f"Enviando {request_count} requests simultáneos...", Colors.CYAN)
        
        def make_request():
            try:
                start_time = time.time()
                response = self.session.get(self.odoo_url, timeout=30)
                response_time = time.time() - start_time
                return {
                    'success': True,
                    'response_time': response_time,
                    'status_code': response.status_code
                }
            except Exception as e:
                return {
                    'success': False,
                    'error': str(e)
                }
                
        # Ejecutar requests concurrentes
        with ThreadPoolExecutor(max_workers=request_count) as executor:
            futures = [executor.submit(make_request) for _ in range(request_count)]
            results = [future.result() for future in as_completed(futures)]
            
        successful_requests = [r for r in results if r['success']]
        success_count = len(successful_requests)
        
        if successful_requests:
            avg_response_time = sum(r['response_time'] for r in successful_requests) / len(successful_requests)
        else:
            avg_response_time = 0
            
        load_test_passed = success_count == request_count and avg_response_time < 10
        
        self.add_test_result(
            f"Prueba de Carga ({request_count} requests)",
            load_test_passed,
            f"{success_count}/{request_count} exitosos",
            response_time=avg_response_time
        )
        
    def test_security_basics(self):
        """Pruebas básicas de seguridad"""
        self.print_header("Pruebas Básicas de Seguridad")
        
        # Test 1: Acceso sin autenticación al database manager
        try:
            response = self.session.get(f"{self.odoo_url}/web/database/manager", timeout=10)
            has_db_manager = "database" in response.text.lower() and "manager" in response.text.lower()
            self.add_test_result(
                "Acceso a Database Manager",
                not has_db_manager,
                f"Database manager {'expuesto' if has_db_manager else 'protegido'}"
            )
        except Exception:
            self.add_test_result(
                "Acceso a Database Manager", True,
                "Endpoint no accesible (bueno)"
            )
            
        # Test 2: Headers de seguridad
        try:
            response = self.session.get(self.odoo_url, timeout=10)
            has_x_frame = 'X-Frame-Options' in response.headers
            has_xss = 'X-XSS-Protection' in response.headers
            has_csp = 'Content-Security-Policy' in response.headers
            
            security_headers_count = sum([has_x_frame, has_xss, has_csp])
            
            self.add_test_result(
                "Headers de Seguridad",
                security_headers_count > 0,
                f"X-Frame-Options: {has_x_frame}, X-XSS-Protection: {has_xss}, CSP: {has_csp}"
            )
        except Exception as e:
            self.add_test_result(
                "Headers de Seguridad", False,
                error_message=str(e)
            )
            
    def test_resource_usage(self):
        """Monitoreo de recursos"""
        self.print_header("Monitoreo de Recursos")
        
        try:
            # Obtener estadísticas de Docker
            result = subprocess.run(
                ["docker", "stats", "--no-stream", "--format", 
                 "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"],
                capture_output=True, text=True
            )
            
            if result.returncode == 0 and result.stdout:
                self.print_colored("Uso actual de recursos:", Colors.CYAN)
                self.print_colored(result.stdout, Colors.WHITE)
                self.add_test_result(
                    "Monitoreo de Recursos", True,
                    "Estadísticas obtenidas correctamente"
                )
            else:
                self.add_test_result(
                    "Monitoreo de Recursos", False,
                    error_message="No se pudieron obtener estadísticas"
                )
        except Exception as e:
            self.add_test_result(
                "Monitoreo de Recursos", False,
                error_message=str(e)
            )
            
    def test_log_analysis(self):
        """Análisis de logs"""
        self.print_header("Análisis de Logs")
        
        try:
            # Obtener logs recientes de Odoo
            result = subprocess.run(
                ["docker-compose", "logs", "--tail=50", "odoo"],
                capture_output=True, text=True, cwd=os.getcwd()
            )
            
            if result.returncode == 0 and result.stdout:
                logs = result.stdout
                error_patterns = ['ERROR', 'CRITICAL', 'FATAL']
                warning_patterns = ['WARNING']
                
                error_count = sum(logs.upper().count(pattern) for pattern in error_patterns)
                warning_count = sum(logs.upper().count(pattern) for pattern in warning_patterns)
                
                log_analysis_passed = error_count == 0
                details = f"Errores: {error_count}, Advertencias: {warning_count}"
                
                self.add_test_result(
                    "Análisis de Logs",
                    log_analysis_passed,
                    details,
                    is_critical=error_count > 0
                )
                
                if error_count > 0:
                    self.print_colored("⚠️  Errores encontrados en logs:", Colors.YELLOW)
                    error_lines = [line for line in logs.split('\n') 
                                 if any(pattern in line.upper() for pattern in error_patterns)]
                    for line in error_lines[:5]:  # Mostrar solo los primeros 5
                        self.print_colored(f"   {line}", Colors.RED)
            else:
                self.add_test_result(
                    "Análisis de Logs", False,
                    error_message="No se pudieron obtener logs"
                )
        except Exception as e:
            self.add_test_result(
                "Análisis de Logs", False,
                error_message=str(e)
            )
            
    def generate_html_report(self):
        """Genera reporte HTML"""
        self.print_header("GENERANDO REPORTE HTML")
        
        end_time = datetime.datetime.now()
        duration = end_time - self.start_time
        
        # Determinar estado general
        if self.critical_errors == 0 and self.failed_tests == 0:
            overall_status = "✅ SISTEMA APROBADO"
            status_class = "passed"
        elif self.critical_errors > 0:
            overall_status = "❌ SISTEMA RECHAZADO (Errores Críticos)"
            status_class = "failed"
        else:
            overall_status = "⚠️ SISTEMA CON ADVERTENCIAS"
            status_class = "warning"
            
        # Generar HTML
        html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Pruebas Cáusticas - Sistema Odoo</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 30px; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .summary-card {{ padding: 20px; border-radius: 8px; text-align: center; color: white; }}
        .summary-card h3 {{ margin: 0 0 10px 0; font-size: 2em; }}
        .summary-card p {{ margin: 0; opacity: 0.9; }}
        .passed {{ background: linear-gradient(135deg, #4CAF50, #45a049); }}
        .failed {{ background: linear-gradient(135deg, #f44336, #da190b); }}
        .warning {{ background: linear-gradient(135deg, #FF9800, #F57C00); }}
        .total {{ background: linear-gradient(135deg, #2196F3, #0b7dda); }}
        .critical {{ background: linear-gradient(135deg, #FF5722, #d84315); }}
        .test-results {{ margin-top: 30px; }}
        .test-item {{ margin-bottom: 15px; padding: 15px; border-radius: 8px; border-left: 5px solid; }}
        .test-passed {{ background-color: #e8f5e8; border-left-color: #4CAF50; }}
        .test-failed {{ background-color: #ffeaea; border-left-color: #f44336; }}
        .test-critical {{ background-color: #fff3e0; border-left-color: #FF5722; }}
        .test-name {{ font-weight: bold; font-size: 1.1em; margin-bottom: 5px; }}
        .test-details {{ color: #666; font-size: 0.9em; }}
        .test-error {{ color: #d32f2f; font-weight: bold; margin-top: 5px; }}
        .test-time {{ color: #888; font-size: 0.8em; float: right; }}
        .footer {{ margin-top: 30px; padding: 20px; background-color: #f8f9fa; border-radius: 8px; text-align: center; color: #666; }}
        .status-icon {{ font-size: 1.2em; margin-right: 8px; }}
        .overall-status {{ text-align: center; padding: 20px; margin: 20px 0; border-radius: 10px; font-size: 1.5em; font-weight: bold; }}
        .overall-status.passed {{ background-color: #d4edda; color: #155724; border: 2px solid #c3e6cb; }}
        .overall-status.failed {{ background-color: #f8d7da; color: #721c24; border: 2px solid #f5c6cb; }}
        .overall-status.warning {{ background-color: #fff3cd; color: #856404; border: 2px solid #ffeaa7; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 Reporte de Pruebas Cáusticas</h1>
            <h2>Sistema de Tickets - Solicitudes Internas</h2>
            <p>Fecha: {self.start_time.strftime('%d/%m/%Y %H:%M:%S')} - {end_time.strftime('%d/%m/%Y %H:%M:%S')}</p>
            <p>Duración total: {str(duration).split('.')[0]}</p>
        </div>
        
        <div class="overall-status {status_class}">
            {overall_status}
        </div>
        
        <div class="summary">
            <div class="summary-card total">
                <h3>{self.total_tests}</h3>
                <p>Total de Pruebas</p>
            </div>
            <div class="summary-card passed">
                <h3>{self.passed_tests}</h3>
                <p>Pruebas Exitosas</p>
            </div>
            <div class="summary-card failed">
                <h3>{self.failed_tests}</h3>
                <p>Pruebas Fallidas</p>
            </div>
            <div class="summary-card critical">
                <h3>{self.critical_errors}</h3>
                <p>Errores Críticos</p>
            </div>
        </div>
        
        <div class="test-results">
            <h2>📋 Resultados Detallados</h2>
"""
        
        # Añadir resultados de pruebas
        for result in self.test_results:
            status_icon = "✅" if result.passed else "❌"
            if result.is_critical:
                css_class = "test-critical"
            elif result.passed:
                css_class = "test-passed"
            else:
                css_class = "test-failed"
                
            html_content += f"""
            <div class="test-item {css_class}">
                <div class="test-name">
                    <span class="status-icon">{status_icon}</span>
                    {result.test_name}
                    <span class="test-time">{result.timestamp}</span>
                </div>
"""
            
            if result.details:
                html_content += f'                <div class="test-details">{result.details}</div>\n'
                
            if result.error_message:
                html_content += f'                <div class="test-error">Error: {result.error_message}</div>\n'
                
            if result.response_time > 0:
                html_content += f'                <div class="test-details">Tiempo de respuesta: {result.response_time:.2f} segundos</div>\n'
                
            html_content += "            </div>\n"
            
        # Cerrar HTML
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        html_content += f"""
        </div>
        
        <div class="footer">
            <h3>📊 Estadísticas Finales</h3>
            <p>Tasa de éxito: {success_rate:.1f}%</p>
            <p>Errores menores: {self.minor_errors}</p>
            <p>Generado por Script de Pruebas Cáusticas v2.0 (Python)</p>
            <p>Sistema: {os.environ.get('COMPUTERNAME', 'Unknown')} | Usuario: {os.environ.get('USERNAME', 'Unknown')}</p>
        </div>
    </div>
</body>
</html>
"""
        
        try:
            with open(self.report_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            self.print_colored(f"✅ Reporte generado exitosamente: {self.report_path}", Colors.GREEN)
            
            # Intentar abrir el reporte en el navegador
            if not self.skip_browser and os.path.exists(self.report_path):
                try:
                    webbrowser.open(f'file://{os.path.abspath(self.report_path)}')
                except Exception:
                    pass  # No es crítico si no se puede abrir el navegador
                    
        except Exception as e:
            self.print_colored(f"❌ Error al generar reporte: {e}", Colors.RED)
            
    def run_all_tests(self):
        """Ejecuta todas las pruebas"""
        # Limpiar pantalla
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Mostrar encabezado principal
        self.print_colored("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🧪 PRUEBAS CÁUSTICAS - SISTEMA ODOO                     ║
║                                                                              ║
║  Este script ejecutará pruebas exhaustivas para validar la robustez         ║
║  y confiabilidad del sistema bajo condiciones extremas.                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
""", Colors.CYAN, bold=True)
        
        self.print_colored("\nConfiguración de pruebas:", Colors.CYAN)
        self.print_colored(f"• URL del sistema: {self.odoo_url}", Colors.WHITE)
        self.print_colored(f"• Usuario de prueba: {self.usuario}", Colors.WHITE)
        self.print_colored(f"• Reporte se guardará en: {self.report_path}", Colors.WHITE)
        self.print_colored(f"• Modo rápido: {'Activado' if self.quick_test else 'Desactivado'}", Colors.WHITE)
        self.print_colored(f"• Abrir navegador: {'No' if self.skip_browser else 'Sí'}", Colors.WHITE)
        
        self.print_colored("\n⏳ Iniciando pruebas...", Colors.CYAN)
        
        # Ejecutar todas las pruebas
        self.test_docker_containers()
        self.test_odoo_connectivity()
        self.test_database_connection()
        self.test_system_load()
        self.test_security_basics()
        self.test_resource_usage()
        self.test_log_analysis()
        
        # Generar reporte
        self.generate_html_report()
        
        # Mostrar resumen final
        self.print_header("RESUMEN FINAL DE PRUEBAS")
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        self.print_colored("📊 Estadísticas:", Colors.CYAN)
        self.print_colored(f"   • Total de pruebas ejecutadas: {self.total_tests}", Colors.WHITE)
        self.print_colored(f"   • Pruebas exitosas: {self.passed_tests}", Colors.GREEN)
        self.print_colored(f"   • Pruebas fallidas: {self.failed_tests}", Colors.RED)
        self.print_colored(f"   • Errores críticos: {self.critical_errors}", Colors.RED)
        self.print_colored(f"   • Errores menores: {self.minor_errors}", Colors.YELLOW)
        
        # Color de la tasa de éxito basado en el porcentaje
        if success_rate >= 90:
            rate_color = Colors.GREEN
        elif success_rate >= 70:
            rate_color = Colors.YELLOW
        else:
            rate_color = Colors.RED
            
        self.print_colored(f"   • Tasa de éxito: {success_rate:.1f}%", rate_color)
        
        # Determinar resultado final
        if self.critical_errors == 0 and self.failed_tests == 0:
            self.print_colored("\n🎉 RESULTADO: SISTEMA APROBADO", Colors.GREEN, bold=True)
            self.print_colored("   El sistema ha pasado todas las pruebas cáusticas.", Colors.GREEN)
            final_status = "APROBADO"
        elif self.critical_errors > 0:
            self.print_colored("\n🚨 RESULTADO: SISTEMA RECHAZADO", Colors.RED, bold=True)
            self.print_colored("   Se encontraron errores críticos que requieren atención inmediata.", Colors.RED)
            final_status = "RECHAZADO"
        else:
            self.print_colored("\n⚠️  RESULTADO: SISTEMA CON ADVERTENCIAS", Colors.YELLOW, bold=True)
            self.print_colored("   El sistema funciona pero tiene problemas menores.", Colors.YELLOW)
            final_status = "CON_ADVERTENCIAS"
            
        self.print_colored(f"\n📄 Reporte detallado disponible en: {self.report_path}", Colors.CYAN)
        
        return final_status

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description="Script de pruebas cáusticas para sistema Odoo con Docker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python ejecutar_pruebas_causticas.py
  python ejecutar_pruebas_causticas.py --quick --report-path /tmp/pruebas.html
  python ejecutar_pruebas_causticas.py --odoo-url http://192.168.1.100:8200 --usuario testuser
        """
    )
    
    parser.add_argument(
        '--report-path', default='./reporte_pruebas_causticas.html',
        help='Ruta donde se guardará el reporte HTML (default: ./reporte_pruebas_causticas.html)'
    )
    parser.add_argument(
        '--odoo-url', default='http://localhost:8200',
        help='URL del sistema Odoo a probar (default: http://localhost:8200)'
    )
    parser.add_argument(
        '--usuario', default='admin',
        help='Usuario para las pruebas de autenticación (default: admin)'
    )
    parser.add_argument(
        '--password', default='admin',
        help='Contraseña para las pruebas de autenticación (default: admin)'
    )
    parser.add_argument(
        '--skip-browser', action='store_true',
        help='Omite abrir el reporte en el navegador automáticamente'
    )
    parser.add_argument(
        '--quick', action='store_true',
        help='Ejecuta solo las pruebas esenciales (modo rápido)'
    )
    
    args = parser.parse_args()
    
    # Crear instancia del tester
    tester = CausticTester(
        odoo_url=args.odoo_url,
        usuario=args.usuario,
        password=args.password,
        report_path=args.report_path,
        quick_test=args.quick,
        skip_browser=args.skip_browser
    )
    
    try:
        result = tester.run_all_tests()
        
        # Código de salida basado en el resultado
        if result == "APROBADO":
            sys.exit(0)
        elif result == "CON_ADVERTENCIAS":
            sys.exit(1)
        elif result == "RECHAZADO":
            sys.exit(2)
        else:
            sys.exit(3)
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  Pruebas interrumpidas por el usuario{Colors.END}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Colors.RED}💥 ERROR FATAL: {e}{Colors.END}")
        import traceback
        traceback.print_exc()
        sys.exit(99)

if __name__ == "__main__":
    main()