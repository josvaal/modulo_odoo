@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM ============================================================================
REM SCRIPT BATCH PARA EJECUTAR PRUEBAS CÁUSTICAS
REM Facilita la ejecución desde el explorador de Windows
REM ============================================================================

title Pruebas Cáusticas - Sistema Odoo
color 0B

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    🧪 PRUEBAS CÁUSTICAS - SISTEMA ODOO                     ║
echo ║                                                                              ║
echo ║  Selecciona el tipo de prueba que deseas ejecutar:                          ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo [1] Pruebas Completas (Recomendado)
echo     - Todas las pruebas exhaustivas
echo     - Genera reporte HTML detallado
echo     - Tiempo estimado: 3-5 minutos
echo.
echo [2] Pruebas Rápidas
echo     - Solo pruebas esenciales
echo     - Genera reporte HTML básico
echo     - Tiempo estimado: 1-2 minutos
echo.
echo [3] Pruebas Simples
echo     - Verificación básica del sistema
echo     - Reporte en texto plano
echo     - Tiempo estimado: 30 segundos
echo.
echo [4] Verificar Estado de Contenedores
echo     - Solo verifica que Docker esté funcionando
echo     - Tiempo estimado: 10 segundos
echo.
echo [5] Ver Logs del Sistema
echo     - Muestra los últimos logs de Odoo
echo.
echo [0] Salir
echo.
set /p opcion="Selecciona una opción (0-5): "

if "%opcion%"=="1" goto pruebas_completas
if "%opcion%"=="2" goto pruebas_rapidas
if "%opcion%"=="3" goto pruebas_simples
if "%opcion%"=="4" goto verificar_contenedores
if "%opcion%"=="5" goto ver_logs
if "%opcion%"=="0" goto salir

echo.
echo ❌ Opción no válida. Intenta de nuevo.
pause
goto inicio

:pruebas_completas
echo.
echo 🚀 Ejecutando pruebas completas...
echo ⏳ Esto puede tomar varios minutos. Por favor espera...
echo.
powershell -ExecutionPolicy Bypass -File "ejecutar_pruebas_causticas.ps1"
set resultado=%ERRORLEVEL%
goto mostrar_resultado

:pruebas_rapidas
echo.
echo ⚡ Ejecutando pruebas rápidas...
echo.
powershell -ExecutionPolicy Bypass -File "ejecutar_pruebas_causticas.ps1" -QuickTest
set resultado=%ERRORLEVEL%
goto mostrar_resultado

:pruebas_simples
echo.
echo 🧪 Ejecutando pruebas simples...
echo.
powershell -ExecutionPolicy Bypass -File "pruebas_causticas_simple.ps1"
set resultado=%ERRORLEVEL%
goto mostrar_resultado_simple

:verificar_contenedores
echo.
echo 🐳 Verificando estado de contenedores Docker...
echo.
docker-compose ps
if %ERRORLEVEL% neq 0 (
    echo.
    echo ❌ Error: No se pudo conectar con Docker o los contenedores no están ejecutándose.
    echo.
    echo 💡 Soluciones posibles:
    echo    1. Asegúrate de que Docker Desktop esté ejecutándose
    echo    2. Ejecuta: docker-compose up -d
    echo    3. Verifica que estés en el directorio correcto
) else (
    echo.
    echo ✅ Contenedores verificados correctamente.
)
echo.
pause
goto inicio

:ver_logs
echo.
echo 📋 Mostrando últimos logs del sistema Odoo...
echo ═══════════════════════════════════════════════════════════════
echo.
docker-compose logs --tail=30 odoo
if %ERRORLEVEL% neq 0 (
    echo.
    echo ❌ Error: No se pudieron obtener los logs.
    echo    Verifica que los contenedores estén ejecutándose.
)
echo.
echo ═══════════════════════════════════════════════════════════════
pause
goto inicio

:mostrar_resultado
echo.
echo ═══════════════════════════════════════════════════════════════
if %resultado%==0 (
    echo ✅ RESULTADO: SISTEMA APROBADO
    echo    Todas las pruebas han sido exitosas.
    color 0A
) else if %resultado%==1 (
    echo ⚠️  RESULTADO: SISTEMA CON ADVERTENCIAS
    echo    El sistema funciona pero tiene problemas menores.
    color 0E
) else if %resultado%==2 (
    echo ❌ RESULTADO: SISTEMA RECHAZADO
    echo    Se encontraron errores críticos.
    color 0C
) else (
    echo 💥 ERROR FATAL durante la ejecución de las pruebas.
    color 0C
)
echo ═══════════════════════════════════════════════════════════════
echo.
echo 📄 Revisa el reporte HTML generado para más detalles.
echo.
set /p continuar="¿Deseas ejecutar otra prueba? (s/n): "
if /i "%continuar%"=="s" (
    color 0B
    goto inicio
) else (
    goto salir
)

:mostrar_resultado_simple
echo.
echo ═══════════════════════════════════════════════════════════════
if %resultado%==0 (
    echo ✅ SISTEMA FUNCIONANDO CORRECTAMENTE
    color 0A
) else if %resultado%==1 (
    echo ⚠️  SISTEMA FUNCIONAL CON ADVERTENCIAS
    color 0E
) else (
    echo 🚨 SISTEMA CON PROBLEMAS SIGNIFICATIVOS
    color 0C
)
echo ═══════════════════════════════════════════════════════════════
echo.
set /p continuar="¿Deseas ejecutar otra prueba? (s/n): "
if /i "%continuar%"=="s" (
    color 0B
    goto inicio
) else (
    goto salir
)

:salir
echo.
echo 👋 ¡Gracias por usar el sistema de pruebas cáusticas!
echo.
pause
exit /b 0

:inicio
cls
color 0B
echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                    🧪 PRUEBAS CÁUSTICAS - SISTEMA ODOO                     ║
echo ║                                                                              ║
echo ║  Selecciona el tipo de prueba que deseas ejecutar:                          ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo [1] Pruebas Completas (Recomendado)
echo     - Todas las pruebas exhaustivas
echo     - Genera reporte HTML detallado
echo     - Tiempo estimado: 3-5 minutos
echo.
echo [2] Pruebas Rápidas
echo     - Solo pruebas esenciales
echo     - Genera reporte HTML básico
echo     - Tiempo estimado: 1-2 minutos
echo.
echo [3] Pruebas Simples
echo     - Verificación básica del sistema
echo     - Reporte en texto plano
echo     - Tiempo estimado: 30 segundos
echo.
echo [4] Verificar Estado de Contenedores
echo     - Solo verifica que Docker esté funcionando
echo     - Tiempo estimado: 10 segundos
echo.
echo [5] Ver Logs del Sistema
echo     - Muestra los últimos logs de Odoo
echo.
echo [0] Salir
echo.
set /p opcion="Selecciona una opción (0-5): "

if "%opcion%"=="1" goto pruebas_completas
if "%opcion%"=="2" goto pruebas_rapidas
if "%opcion%"=="3" goto pruebas_simples
if "%opcion%"=="4" goto verificar_contenedores
if "%opcion%"=="5" goto ver_logs
if "%opcion%"=="0" goto salir

echo.
echo ❌ Opción no válida. Intenta de nuevo.
pause
goto inicio