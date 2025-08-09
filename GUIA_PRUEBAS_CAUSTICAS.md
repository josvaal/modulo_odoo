# 🧪 Guía de Pruebas Cáusticas - Sistema Odoo

## 📋 Índice

1. [¿Qué son las Pruebas Cáusticas?](#qué-son-las-pruebas-cáusticas)
2. [Archivos de Pruebas Disponibles](#archivos-de-pruebas-disponibles)
3. [Métodos de Ejecución](#métodos-de-ejecución)
4. [Tipos de Pruebas](#tipos-de-pruebas)
5. [Interpretación de Resultados](#interpretación-de-resultados)
6. [Solución de Problemas](#solución-de-problemas)
7. [Automatización](#automatización)

---

## 🎯 ¿Qué son las Pruebas Cáusticas?

Las **pruebas cáusticas** son pruebas exhaustivas diseñadas para "romper" el sistema y encontrar sus límites. Su objetivo es:

- ✅ **Validar la robustez** del sistema bajo condiciones extremas
- ✅ **Identificar puntos de falla** antes de que ocurran en producción
- ✅ **Verificar la recuperación** automática del sistema
- ✅ **Medir el rendimiento** bajo carga
- ✅ **Detectar vulnerabilidades** de seguridad básicas

> **💡 Importante**: Estas pruebas deben ejecutarse en un entorno de desarrollo o testing, **NUNCA en producción**.

---

## 📁 Archivos de Pruebas Disponibles

### 🚀 Scripts Principales

| Archivo | Descripción | Tiempo Estimado | Nivel |
|---------|-------------|-----------------|-------|
| `ejecutar_pruebas.bat` | **Menú interactivo** - Fácil de usar | Variable | Principiante |
| `ejecutar_pruebas_causticas.ps1` | **Pruebas completas** con reporte HTML | 3-5 min | Avanzado |
| `pruebas_causticas_simple.ps1` | **Pruebas básicas** rápidas | 30 seg | Intermedio |

### 📄 Archivos de Documentación

- `GUIA_PRUEBAS_CAUSTICAS.md` - Esta guía
- `README.md` - Manual completo del sistema

---

## 🖱️ Métodos de Ejecución

### Método 1: Interfaz Gráfica (Recomendado para Principiantes)

1. **Doble clic** en `ejecutar_pruebas.bat`
2. Selecciona el tipo de prueba desde el menú
3. Espera a que termine la ejecución
4. Revisa los resultados en pantalla

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🧪 PRUEBAS CÁUSTICAS - SISTEMA ODOO                     ║
║                                                                              ║
║  Selecciona el tipo de prueba que deseas ejecutar:                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

[1] Pruebas Completas (Recomendado)
[2] Pruebas Rápidas  
[3] Pruebas Simples
[4] Verificar Estado de Contenedores
[5] Ver Logs del Sistema
[0] Salir
```

### Método 2: PowerShell (Para Usuarios Avanzados)

#### Pruebas Completas
```powershell
# Navegar al directorio del proyecto
cd [RUTA_DE_TU_PROYECTO]\modulo_odoo

# Ejecutar pruebas completas
.\ejecutar_pruebas_causticas.ps1

# Con parámetros personalizados
.\ejecutar_pruebas_causticas.ps1 -QuickTest -ReportPath "C:\Reports\mi_reporte.html"
```

#### Pruebas Simples
```powershell
# Pruebas básicas rápidas
.\pruebas_causticas_simple.ps1

# Con URL personalizada
.\pruebas_causticas_simple.ps1 -OdooUrl "http://192.168.1.100:8200"
```

### Método 3: Línea de Comandos

```cmd
# Desde CMD o PowerShell
cd [RUTA_DE_TU_PROYECTO]\modulo_odoo
powershell -ExecutionPolicy Bypass -File "ejecutar_pruebas_causticas.ps1"
```

---

## 🔬 Tipos de Pruebas

### 🔥 Pruebas de Estrés y Límites

| Prueba | Descripción | Objetivo |
|--------|-------------|----------|
| **Volumen de Solicitudes** | 100+ solicitudes simultáneas | Probar rendimiento con alta carga |
| **Datos Extremos** | Títulos de 1000+ caracteres | Validar límites de campos |
| **Archivos Grandes** | Subir archivos >50MB | Probar manejo de archivos |

### 💥 Pruebas de Casos Extremos

| Prueba | Descripción | Objetivo |
|--------|-------------|----------|
| **Estados Inválidos** | Transiciones no permitidas | Validar lógica de negocio |
| **Fechas Extremas** | Fechas en el pasado/futuro | Probar validaciones temporales |
| **Permisos** | Acceso no autorizado | Verificar seguridad |

### 🌐 Pruebas de Compatibilidad

| Prueba | Descripción | Objetivo |
|--------|-------------|----------|
| **Navegadores** | Chrome, Firefox, Edge, Safari | Compatibilidad cross-browser |
| **Responsividad** | Pantallas pequeñas/grandes | Adaptabilidad de UI |
| **Zoom** | 50% y 200% | Accesibilidad |

### 🔒 Pruebas de Seguridad

| Prueba | Descripción | Objetivo |
|--------|-------------|----------|
| **Inyección** | HTML/JavaScript/SQL | Prevenir ataques |
| **Autenticación** | Credenciales incorrectas | Validar acceso |
| **Sesiones** | Timeout y concurrencia | Gestión de sesiones |

---

## 📊 Interpretación de Resultados

### 🎯 Códigos de Salida

| Código | Estado | Significado | Acción Requerida |
|--------|--------|-------------|------------------|
| **0** | ✅ APROBADO | Todas las pruebas pasaron | Ninguna |
| **1** | ⚠️ CON ADVERTENCIAS | Problemas menores | Revisar y corregir |
| **2** | ❌ RECHAZADO | Errores críticos | Corrección inmediata |
| **99** | 💥 ERROR FATAL | Fallo del script | Revisar configuración |

### 📈 Métricas de Rendimiento

#### ✅ Benchmarks Aceptables
- **Carga inicial**: < 3 segundos
- **Creación de solicitud**: < 2 segundos
- **Búsqueda/filtrado**: < 1 segundo
- **Reportes**: < 10 segundos
- **Subida de archivos (10MB)**: < 30 segundos

#### ⚠️ Señales de Alerta
- Tiempo de respuesta > 5 segundos
- Errores en logs
- Uso de memoria > 80%
- Fallos en pruebas de carga

### 📄 Tipos de Reportes

#### Reporte HTML Completo
- **Ubicación**: `reporte_pruebas_causticas.html`
- **Contenido**: Resultados detallados, gráficos, estadísticas
- **Se abre automáticamente** en el navegador

#### Reporte Simple (Texto)
- **Ubicación**: `reporte_simple_YYYYMMDD_HHMMSS.txt`
- **Contenido**: Resumen básico de resultados
- **Ideal para**: Logs automáticos

---

## 🛠️ Solución de Problemas

### ❌ Problemas Comunes

#### "No se puede ejecutar scripts en este sistema"
```powershell
# Solución: Cambiar política de ejecución
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### "Docker no responde"
```powershell
# Verificar estado de Docker
docker --version
docker-compose --version

# Reiniciar contenedores
docker-compose down
docker-compose up -d
```

#### "Sistema no accesible en localhost:8200"
```powershell
# Verificar puertos
netstat -an | findstr :8200

# Verificar contenedores
docker-compose ps

# Ver logs
docker-compose logs odoo
```

### 🔧 Comandos de Diagnóstico

```powershell
# Estado general del sistema
docker-compose ps
docker stats --no-stream

# Logs detallados
docker-compose logs --tail=50 odoo
docker-compose logs --tail=50 db

# Conectividad
Test-NetConnection localhost -Port 8200
Test-NetConnection localhost -Port 5432

# Recursos del sistema
Get-Process | Where-Object {$_.ProcessName -like "*docker*"}
```

---

## 🤖 Automatización

### 📅 Ejecución Programada

#### Usando Programador de Tareas de Windows

1. Abrir **Programador de tareas**
2. Crear **Tarea básica**
3. Configurar:
   - **Nombre**: "Pruebas Cáusticas Odoo"
   - **Frecuencia**: Diaria/Semanal
   - **Acción**: Iniciar programa
   - **Programa**: `powershell.exe`
   - **Argumentos**: `-ExecutionPolicy Bypass -File "C:\ruta\ejecutar_pruebas_causticas.ps1" -QuickTest`

#### Script de Automatización

```powershell
# Crear archivo: automatizar_pruebas.ps1
$logFile = "pruebas_automaticas_$(Get-Date -Format 'yyyyMMdd').log"

try {
    Write-Output "[$(Get-Date)] Iniciando pruebas automáticas" | Tee-Object -FilePath $logFile -Append
    
    & ".\ejecutar_pruebas_causticas.ps1" -QuickTest
    $resultado = $LASTEXITCODE
    
    Write-Output "[$(Get-Date)] Pruebas completadas. Código: $resultado" | Tee-Object -FilePath $logFile -Append
    
    if ($resultado -ne 0) {
        # Enviar notificación o email de alerta
        Write-Output "[$(Get-Date)] ALERTA: Sistema con problemas" | Tee-Object -FilePath $logFile -Append
    }
} catch {
    Write-Output "[$(Get-Date)] ERROR: $($_.Exception.Message)" | Tee-Object -FilePath $logFile -Append
}
```

### 📧 Notificaciones por Email

```powershell
# Agregar al final del script principal
if ($Global:CriticalErrors -gt 0) {
    $emailParams = @{
        To = "admin@empresa.com"
        From = "sistema@empresa.com"
        Subject = "🚨 ALERTA: Errores críticos en sistema Odoo"
        Body = "Se encontraron $Global:CriticalErrors errores críticos. Revisar reporte adjunto."
        SmtpServer = "smtp.empresa.com"
        Attachments = $ReportPath
    }
    
    try {
        Send-MailMessage @emailParams
        Write-Host "📧 Notificación enviada por email" -ForegroundColor Green
    } catch {
        Write-Host "❌ Error enviando email: $($_.Exception.Message)" -ForegroundColor Red
    }
}
```

---

## 📚 Ejemplos de Uso

### Escenario 1: Verificación Diaria
```powershell
# Ejecutar pruebas simples cada mañana
.\pruebas_causticas_simple.ps1
```

### Escenario 2: Antes de Despliegue
```powershell
# Pruebas completas antes de actualizar producción
.\ejecutar_pruebas_causticas.ps1 -ReportPath "pre_deploy_$(Get-Date -Format 'yyyyMMdd').html"
```

### Escenario 3: Investigación de Problemas
```powershell
# Pruebas detalladas cuando hay reportes de lentitud
.\ejecutar_pruebas_causticas.ps1 -OdooUrl "http://servidor-problema:8200"
```

### Escenario 4: Validación de Configuración
```powershell
# Después de cambios en docker-compose.yaml
.\ejecutar_pruebas.bat
# Seleccionar opción [4] para verificar contenedores
```

---

## 🎓 Mejores Prácticas

### ✅ Recomendaciones

1. **Ejecutar regularmente**: Al menos una vez por semana
2. **Documentar resultados**: Mantener historial de reportes
3. **Actuar sobre advertencias**: No ignorar problemas menores
4. **Probar después de cambios**: Siempre validar modificaciones
5. **Mantener actualizado**: Revisar y mejorar las pruebas

### ❌ Evitar

1. **No ejecutar en producción**: Solo en desarrollo/testing
2. **No ignorar errores críticos**: Requieren atención inmediata
3. **No sobrecargar**: Espaciar las pruebas de carga
4. **No modificar scripts sin entender**: Pueden afectar la validez

---

## 📞 Soporte

Si encuentras problemas con las pruebas:

1. **Revisa esta guía** completa
2. **Consulta el README.md** principal
3. **Verifica los logs** del sistema
4. **Documenta el error** con capturas de pantalla
5. **Incluye el reporte** generado al reportar problemas

---

**💡 Recuerda**: Las pruebas cáusticas son una herramienta preventiva. Un sistema que pasa estas pruebas es un sistema confiable para producción.

---

*Última actualización: $(Get-Date -Format 'dd/MM/yyyy')*