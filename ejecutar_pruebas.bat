@echo off
setlocal enabledelayedexpansion

REM ============================================================================
REM SCRIPT BATCH PARA EJECUTAR PRUEBAS CAUSTICAS
REM Facilita la ejecucion desde el explorador de Windows
REM ============================================================================

:inicio
title Pruebas Causticas - Sistema Odoo
color 0B
cls

echo.
echo ===============================================================================
echo                     PRUEBAS CAUSTICAS - SISTEMA ODOO
echo.
echo   Selecciona el tipo de prueba que deseas ejecutar:
echo ===============================================================================
echo.
echo [1] Pruebas Completas (Recomendado)
echo     - Todas las pruebas exhaustivas
echo     - Genera reporte HTML detallado
echo     - Tiempo estimado: 3-5 minutos
echo.
echo [2] Pruebas Rapidas
echo     - Solo pruebas esenciales
echo     - Genera reporte HTML basico
echo     - Tiempo estimado: 1-2 minutos
echo.
echo [3] Pruebas Simples
echo     - Verificacion basica del sistema
echo     - Reporte en texto plano
echo     - Tiempo estimado: 30 segundos
echo.
echo [4] Verificar Estado de Contenedores
echo     - Solo verifica que Docker este funcionando
echo     - Tiempo estimado: 10 segundos
echo.
echo [5] Ver Logs del Sistema
echo     - Muestra los ultimos logs de Odoo
echo.
echo [0] Salir
echo.
set /p opcion="Selecciona una opcion (0-5): "

if "%opcion%"=="1" goto pruebas_completas
if "%opcion%"=="2" goto pruebas_rapidas
if "%opcion%"=="3" goto pruebas_simples
if "%opcion%"=="4" goto verificar_contenedores
if "%opcion%"=="5" goto ver_logs
if "%opcion%"=="0" goto salir

goto opcion_invalida

:pruebas_completas
echo.
echo Ejecutando pruebas completas...
echo Esto puede tomar varios minutos. Por favor espera...
echo.
powershell -ExecutionPolicy Bypass -File "ejecutar_pruebas_causticas.ps1"
set resultado=%ERRORLEVEL%
goto mostrar_resultado

:pruebas_rapidas
echo.
echo Ejecutando pruebas rapidas...
echo.
powershell -ExecutionPolicy Bypass -File "ejecutar_pruebas_causticas.ps1" -QuickTest
set resultado=%ERRORLEVEL%
goto mostrar_resultado

:pruebas_simples
echo.
echo Ejecutando pruebas simples...
echo.
powershell -ExecutionPolicy Bypass -File "pruebas_causticas_simple.ps1"
set resultado=%ERRORLEVEL%
goto mostrar_resultado_simple

:verificar_contenedores
echo.
echo Verificando estado de contenedores Docker...
echo.
docker-compose ps
if %ERRORLEVEL% neq 0 (
    echo.
    echo Error: No se pudo conectar con Docker o los contenedores no estan ejecutandose.
    echo.
    echo Soluciones posibles:
    echo    1. Asegurate de que Docker Desktop este ejecutandose
    echo    2. Ejecuta: docker-compose up -d
    echo    3. Verifica que estes en el directorio correcto
) else (
    echo.
    echo Contenedores verificados correctamente.
)
echo.
pause
goto inicio

:ver_logs
echo.
echo Mostrando ultimos logs del sistema Odoo...
echo ===============================================================================
echo.
docker-compose logs --tail=30 odoo
if %ERRORLEVEL% neq 0 (
    echo.
    echo Error: No se pudieron obtener los logs.
    echo    Verifica que los contenedores esten ejecutandose.
)
echo.
echo ===============================================================================
pause
goto inicio

:mostrar_resultado
echo.
echo ===============================================================================
echo                    RESULTADO DE LAS PRUEBAS
echo ===============================================================================
echo.
if %resultado%==0 (
    echo APROBADO: Todas las pruebas pasaron exitosamente.
    echo    El sistema esta funcionando correctamente.
) else if %resultado%==1 (
    echo ADVERTENCIAS: Algunas pruebas mostraron advertencias.
    echo    El sistema funciona pero requiere atencion.
) else (
    echo RECHAZADO: Algunas pruebas fallaron.
    echo    El sistema requiere correccion inmediata.
)
echo.
echo Revisa el reporte HTML generado para mas detalles.
echo ===============================================================================
echo.
pause
goto inicio

:mostrar_resultado_simple
echo.
echo ===============================================================================
echo                    RESULTADO DE PRUEBAS SIMPLES
echo ===============================================================================
echo.
if %resultado%==0 (
    echo APROBADO: Pruebas basicas completadas exitosamente.
) else if %resultado%==1 (
    echo ADVERTENCIAS: Algunas verificaciones mostraron advertencias.
) else (
    echo RECHAZADO: Algunas verificaciones fallaron.
)
echo.
echo Revisa el archivo de reporte generado para mas detalles.
echo ===============================================================================
echo.
pause
goto inicio

:opcion_invalida
echo.
echo Opcion no valida. Por favor selecciona una opcion del 0 al 5.
echo.
pause
goto inicio

:salir
echo.
echo Gracias por usar el sistema de pruebas causticas!
echo.
exit /b 0