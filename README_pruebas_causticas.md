# 🧪 Script de Pruebas Cáusticas - Sistema Odoo

## Descripción

Este script ejecuta pruebas exhaustivas ("cáusticas") para validar la robustez y confiabilidad del sistema Odoo bajo condiciones extremas. Ha sido completamente reescrito en Python para mayor flexibilidad y mantenibilidad.

## Características

- ✅ **Pruebas de conectividad** - Verifica que el sistema responda correctamente
- 🐳 **Verificación de Docker** - Comprueba el estado de todos los contenedores
- 🗄️ **Conexión a base de datos** - Valida la conectividad con PostgreSQL
- ⚡ **Pruebas de carga** - Envía múltiples requests simultáneos
- 🔒 **Seguridad básica** - Verifica headers de seguridad y exposición de endpoints
- 📊 **Monitoreo de recursos** - Analiza el uso de CPU y memoria
- 📝 **Análisis de logs** - Busca errores y advertencias en los logs
- 📄 **Reporte HTML** - Genera un reporte detallado y visualmente atractivo

## Requisitos

### Sistema
- Python 3.8 o superior
- Docker y Docker Compose instalados
- Sistema Odoo ejecutándose en contenedores

### Dependencias Python
```bash
pip install -r requirements.txt
```

O instalar manualmente:
```bash
pip install requests psycopg2-binary colorama jsonschema
```

## Instalación

1. **Clonar o descargar** el script en tu directorio del proyecto
2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Verificar que Docker esté ejecutándose** y que los contenedores de Odoo estén activos

## Uso

### Uso básico
```bash
python ejecutar_pruebas_causticas.py
```

### Opciones avanzadas
```bash
# Modo rápido (solo pruebas esenciales)
python ejecutar_pruebas_causticas.py --quick

# Especificar URL personalizada
python ejecutar_pruebas_causticas.py --odoo-url http://192.168.1.100:8200

# Cambiar ruta del reporte
python ejecutar_pruebas_causticas.py --report-path /tmp/mi_reporte.html

# No abrir navegador automáticamente
python ejecutar_pruebas_causticas.py --skip-browser

# Usar credenciales personalizadas
python ejecutar_pruebas_causticas.py --usuario testuser --password testpass
```

### Parámetros disponibles

| Parámetro | Descripción | Valor por defecto |
|-----------|-------------|-------------------|
| `--odoo-url` | URL del sistema Odoo | `http://localhost:8200` |
| `--usuario` | Usuario para pruebas de autenticación | `admin` |
| `--password` | Contraseña para pruebas | `admin` |
| `--report-path` | Ruta del reporte HTML | `./reporte_pruebas_causticas.html` |
| `--quick` | Modo rápido (omite pruebas de carga) | `False` |
| `--skip-browser` | No abrir navegador automáticamente | `False` |

## Tipos de Pruebas

### 1. Verificación de Contenedores Docker
- Comprueba que todos los contenedores estén ejecutándose
- Identifica contenedores detenidos o con errores
- **Crítico**: Si algún contenedor esencial no está ejecutándose

### 2. Prueba de Conectividad HTTP
- Verifica que el servidor Odoo responda
- Mide tiempo de respuesta
- **Crítico**: Si el servidor no responde o devuelve errores HTTP

### 3. Conexión a Base de Datos
- Usa `pg_isready` para verificar PostgreSQL
- Intenta conexión directa si `psycopg2` está disponible
- **Crítico**: Si la base de datos no está accesible

### 4. Pruebas de Carga
- Envía múltiples requests simultáneos (configurable)
- Mide tiempo de respuesta promedio
- **Omitida en modo rápido**
- **Falla**: Si el tiempo de respuesta promedio > 10 segundos

### 5. Seguridad Básica
- Verifica que el Database Manager no esté expuesto
- Comprueba headers de seguridad (X-Frame-Options, CSP, etc.)
- **Advertencia**: Si faltan headers de seguridad

### 6. Monitoreo de Recursos
- Obtiene estadísticas de uso de CPU y memoria de Docker
- Muestra información en tiempo real
- **Informativo**: No genera fallos críticos

### 7. Análisis de Logs
- Busca patrones de ERROR, CRITICAL, FATAL en logs recientes
- Cuenta advertencias (WARNING)
- **Crítico**: Si encuentra errores en los logs

## Interpretación de Resultados

### Códigos de Salida
- `0`: ✅ **SISTEMA APROBADO** - Todas las pruebas pasaron
- `1`: ⚠️ **SISTEMA CON ADVERTENCIAS** - Funciona pero tiene problemas menores
- `2`: ❌ **SISTEMA RECHAZADO** - Errores críticos encontrados
- `3`: 💥 **ERROR DESCONOCIDO** - Error inesperado en el script
- `99`: 💥 **ERROR FATAL** - Excepción no controlada
- `130`: ⚠️ **INTERRUMPIDO** - Usuario canceló la ejecución

### Tipos de Errores
- **Críticos**: Impiden el funcionamiento normal del sistema
- **Menores**: Problemas que no afectan la funcionalidad básica
- **Advertencias**: Recomendaciones de mejora

## Reporte HTML

El script genera un reporte HTML completo que incluye:

- 📊 **Dashboard visual** con estadísticas generales
- 📋 **Resultados detallados** de cada prueba
- ⏱️ **Tiempos de respuesta** y timestamps
- 🎨 **Código de colores** para fácil interpretación
- 📱 **Diseño responsivo** para visualización en móviles

### Abrir el reporte
Por defecto, el reporte se abre automáticamente en tu navegador. Para desactivar esto:
```bash
python ejecutar_pruebas_causticas.py --skip-browser
```

## Integración con CI/CD

### GitHub Actions
```yaml
- name: Ejecutar Pruebas Cáusticas
  run: |
    pip install -r requirements.txt
    python ejecutar_pruebas_causticas.py --skip-browser --quick
  continue-on-error: false
```

### Jenkins
```groovy
stage('Pruebas Cáusticas') {
    steps {
        sh 'pip install -r requirements.txt'
        sh 'python ejecutar_pruebas_causticas.py --skip-browser'
    }
    post {
        always {
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: '.',
                reportFiles: 'reporte_pruebas_causticas.html',
                reportName: 'Reporte Pruebas Cáusticas'
            ])
        }
    }
}
```

## Solución de Problemas

### Error: "requests no está instalado"
```bash
pip install requests
```

### Error: "docker-compose no encontrado"
- Verifica que Docker Compose esté instalado
- En sistemas nuevos, usa `docker compose` (sin guión)

### Error: "No se pudieron obtener logs"
- Verifica que estés en el directorio correcto del proyecto
- Comprueba que `docker-compose.yml` exista

### Advertencia: "psycopg2 no está instalado"
- Las pruebas de BD serán limitadas pero funcionales
- Para pruebas completas: `pip install psycopg2-binary`

### Pruebas de carga fallan
- Verifica que el sistema no esté sobrecargado
- Usa `--quick` para omitir estas pruebas
- Ajusta el timeout si la red es lenta

## Personalización

### Modificar número de requests en pruebas de carga
Edita la variable `request_count` en el método `test_system_load()`:
```python
request_count = 20  # Cambiar de 10 a 20
```

### Añadir nuevas pruebas
1. Crea un nuevo método `test_mi_nueva_prueba()`
2. Añádelo a `run_all_tests()`
3. Usa `self.add_test_result()` para registrar resultados

### Personalizar reporte HTML
Modifica el método `generate_html_report()` para cambiar:
- Estilos CSS
- Estructura del reporte
- Información adicional

## Migración desde PowerShell

Este script reemplaza completamente la versión anterior en PowerShell, ofreciendo:

- ✅ **Mejor manejo de errores**
- ✅ **Código más mantenible**
- ✅ **Multiplataforma** (Windows, Linux, macOS)
- ✅ **Mejor integración con CI/CD**
- ✅ **Reportes más detallados**
- ✅ **Pruebas concurrentes**
- ✅ **Configuración más flexible**

## Contribuir

Para contribuir al desarrollo:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Añade pruebas para nuevas funcionalidades
4. Asegúrate de que el código siga PEP 8
5. Envía un Pull Request

## Licencia

Este script es de uso interno para el proyecto de Sistema de Tickets - Solicitudes Internas.

---

**Versión**: 2.0  
**Autor**: Sistema de Pruebas Automatizadas  
**Última actualización**: $(date)