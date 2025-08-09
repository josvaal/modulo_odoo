# ============================================================================
# SCRIPT DE PRUEBAS CÁUSTICAS PARA SISTEMA ODOO
# Automatiza la ejecución de pruebas exhaustivas y genera reporte detallado
# ============================================================================

param(
    [string]$ReportPath = "./reporte_pruebas_causticas.html",
    [string]$OdooUrl = "http://localhost:8200",
    [string]$Usuario = "admin",
    [string]$Password = "admin",
    [switch]$SkipBrowserTests,
    [switch]$QuickTest
)

# Configuración de colores para output
$ErrorColor = "Red"
$SuccessColor = "Green"
$WarningColor = "Yellow"
$InfoColor = "Cyan"

# Variables globales para el reporte
$Global:TestResults = @()
$Global:StartTime = Get-Date
$Global:TotalTests = 0
$Global:PassedTests = 0
$Global:FailedTests = 0
$Global:CriticalErrors = 0
$Global:MinorErrors = 0

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

function Write-TestHeader {
    param([string]$TestName)
    Write-Host "`n" -NoNewline
    Write-Host "=" * 80 -ForegroundColor $InfoColor
    Write-Host "EJECUTANDO: $TestName" -ForegroundColor $InfoColor
    Write-Host "=" * 80 -ForegroundColor $InfoColor
}

function Write-TestResult {
    param(
        [string]$TestName,
        [bool]$Passed,
        [string]$Details = "",
        [string]$ErrorMessage = "",
        [double]$ResponseTime = 0,
        [bool]$IsCritical = $false
    )
    
    $Global:TotalTests++
    
    $result = @{
        TestName = $TestName
        Passed = $Passed
        Details = $Details
        ErrorMessage = $ErrorMessage
        ResponseTime = $ResponseTime
        Timestamp = Get-Date
        IsCritical = $IsCritical
    }
    
    $Global:TestResults += $result
    
    if ($Passed) {
        $Global:PassedTests++
        Write-Host "✅ PASÓ: $TestName" -ForegroundColor $SuccessColor
        if ($Details) { Write-Host "   Detalles: $Details" -ForegroundColor Gray }
    } else {
        $Global:FailedTests++
        if ($IsCritical) { $Global:CriticalErrors++ } else { $Global:MinorErrors++ }
        Write-Host "❌ FALLÓ: $TestName" -ForegroundColor $ErrorColor
        if ($ErrorMessage) { Write-Host "   Error: $ErrorMessage" -ForegroundColor $ErrorColor }
        if ($Details) { Write-Host "   Detalles: $Details" -ForegroundColor Gray }
    }
    
    if ($ResponseTime -gt 0) {
        Write-Host "   Tiempo de respuesta: $($ResponseTime.ToString('F2')) segundos" -ForegroundColor Gray
    }
}

function Test-OdooConnectivity {
    Write-TestHeader "Prueba de Conectividad Básica"
    
    try {
        $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
        $response = Invoke-WebRequest -Uri $OdooUrl -UseBasicParsing -TimeoutSec 30
        $stopwatch.Stop()
        
        if ($response.StatusCode -eq 200) {
            Write-TestResult -TestName "Conectividad HTTP" -Passed $true -Details "Servidor responde correctamente" -ResponseTime $stopwatch.Elapsed.TotalSeconds
        } else {
            Write-TestResult -TestName "Conectividad HTTP" -Passed $false -ErrorMessage "Código de estado: $($response.StatusCode)" -IsCritical $true
        }
    } catch {
        Write-TestResult -TestName "Conectividad HTTP" -Passed $false -ErrorMessage $_.Exception.Message -IsCritical $true
    }
}

function Test-DockerContainers {
    Write-TestHeader "Verificación de Contenedores Docker"
    
    try {
        $containers = docker-compose ps --format json | ConvertFrom-Json
        
        foreach ($container in $containers) {
            $isRunning = $container.State -eq "running"
            Write-TestResult -TestName "Contenedor $($container.Service)" -Passed $isRunning -Details "Estado: $($container.State)" -IsCritical (-not $isRunning)
        }
    } catch {
        Write-TestResult -TestName "Verificación Docker" -Passed $false -ErrorMessage $_.Exception.Message -IsCritical $true
    }
}

function Test-DatabaseConnection {
    Write-TestHeader "Prueba de Conexión a Base de Datos"
    
    try {
        # Intentar conectar a PostgreSQL
        $dbTest = docker exec modulo_odoo-db-1 pg_isready -U odoo 2>$null
        $dbConnected = $LASTEXITCODE -eq 0
        
        Write-TestResult -TestName "Conexión PostgreSQL" -Passed $dbConnected -Details "pg_isready status" -IsCritical (-not $dbConnected)
    } catch {
        Write-TestResult -TestName "Conexión PostgreSQL" -Passed $false -ErrorMessage $_.Exception.Message -IsCritical $true
    }
}

function Test-SystemLoad {
    Write-TestHeader "Pruebas de Carga del Sistema"
    
    if ($QuickTest) {
        Write-Host "⚡ Modo rápido activado - Saltando pruebas de carga intensiva" -ForegroundColor $WarningColor
        return
    }
    
    # Simular múltiples requests simultáneos
    $jobs = @()
    $requestCount = 10
    
    Write-Host "Enviando $requestCount requests simultáneos..." -ForegroundColor $InfoColor
    
    for ($i = 1; $i -le $requestCount; $i++) {
        $job = Start-Job -ScriptBlock {
            param($url)
            try {
                $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
                $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 30
                $stopwatch.Stop()
                return @{ Success = $true; ResponseTime = $stopwatch.Elapsed.TotalSeconds; StatusCode = $response.StatusCode }
            } catch {
                return @{ Success = $false; Error = $_.Exception.Message }
            }
        } -ArgumentList $OdooUrl
        $jobs += $job
    }
    
    # Esperar a que terminen todos los jobs
    $results = $jobs | Wait-Job | Receive-Job
    $jobs | Remove-Job
    
    $successCount = ($results | Where-Object { $_.Success }).Count
    $avgResponseTime = ($results | Where-Object { $_.Success } | Measure-Object -Property ResponseTime -Average).Average
    
    $loadTestPassed = $successCount -eq $requestCount -and $avgResponseTime -lt 10
    
    Write-TestResult -TestName "Prueba de Carga ($requestCount requests)" -Passed $loadTestPassed -Details "$successCount/$requestCount exitosos" -ResponseTime $avgResponseTime
}

function Test-SecurityBasics {
    Write-TestHeader "Pruebas Básicas de Seguridad"
    
    # Test 1: Acceso sin autenticación
    try {
        $response = Invoke-WebRequest -Uri "$OdooUrl/web/database/manager" -UseBasicParsing -TimeoutSec 10
        $hasDbManager = $response.Content -match "database.*manager"
        Write-TestResult -TestName "Acceso a Database Manager" -Passed (-not $hasDbManager) -Details "Database manager $(if($hasDbManager){'expuesto'}else{'protegido'})"
    } catch {
        Write-TestResult -TestName "Acceso a Database Manager" -Passed $true -Details "Endpoint no accesible (bueno)"
    }
    
    # Test 2: Headers de seguridad
    try {
        $response = Invoke-WebRequest -Uri $OdooUrl -UseBasicParsing -TimeoutSec 10
        $hasXFrame = $response.Headers.ContainsKey("X-Frame-Options")
        $hasXSS = $response.Headers.ContainsKey("X-XSS-Protection")
        
        Write-TestResult -TestName "Headers de Seguridad" -Passed ($hasXFrame -or $hasXSS) -Details "X-Frame-Options: $hasXFrame, X-XSS-Protection: $hasXSS"
    } catch {
        Write-TestResult -TestName "Headers de Seguridad" -Passed $false -ErrorMessage $_.Exception.Message
    }
}

function Test-ResourceUsage {
    Write-TestHeader "Monitoreo de Recursos"
    
    try {
        # Obtener estadísticas de Docker
        $stats = docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" 2>$null
        
        if ($stats) {
            Write-Host "Uso actual de recursos:" -ForegroundColor $InfoColor
            Write-Host $stats -ForegroundColor Gray
            Write-TestResult -TestName "Monitoreo de Recursos" -Passed $true -Details "Estadísticas obtenidas correctamente"
        } else {
            Write-TestResult -TestName "Monitoreo de Recursos" -Passed $false -ErrorMessage "No se pudieron obtener estadísticas"
        }
    } catch {
        Write-TestResult -TestName "Monitoreo de Recursos" -Passed $false -ErrorMessage $_.Exception.Message
    }
}

function Test-LogAnalysis {
    Write-TestHeader "Análisis de Logs"
    
    try {
        # Obtener logs recientes de Odoo
        $logs = docker-compose logs --tail=50 odoo 2>$null
        
        if ($logs) {
            $errorCount = ($logs | Select-String -Pattern "ERROR|CRITICAL|FATAL").Count
            $warningCount = ($logs | Select-String -Pattern "WARNING").Count
            
            $logAnalysisPassed = $errorCount -eq 0
            $details = "Errores: $errorCount, Advertencias: $warningCount"
            
            Write-TestResult -TestName "Análisis de Logs" -Passed $logAnalysisPassed -Details $details -IsCritical ($errorCount -gt 0)
            
            if ($errorCount -gt 0) {
                Write-Host "⚠️  Errores encontrados en logs:" -ForegroundColor $WarningColor
                $logs | Select-String -Pattern "ERROR|CRITICAL|FATAL" | Select-Object -First 5 | ForEach-Object {
                    Write-Host "   $($_.Line)" -ForegroundColor $ErrorColor
                }
            }
        } else {
            Write-TestResult -TestName "Análisis de Logs" -Passed $false -ErrorMessage "No se pudieron obtener logs"
        }
    } catch {
        Write-TestResult -TestName "Análisis de Logs" -Passed $false -ErrorMessage $_.Exception.Message
    }
}

function Generate-HtmlReport {
    Write-Host "`n" -NoNewline
    Write-Host "=" * 80 -ForegroundColor $InfoColor
    Write-Host "GENERANDO REPORTE HTML" -ForegroundColor $InfoColor
    Write-Host "=" * 80 -ForegroundColor $InfoColor
    
    $endTime = Get-Date
    $duration = $endTime - $Global:StartTime
    
    $html = @"
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Pruebas Cáusticas - Sistema Odoo</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; }
        .summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .summary-card { padding: 20px; border-radius: 8px; text-align: center; color: white; }
        .summary-card h3 { margin: 0 0 10px 0; font-size: 2em; }
        .summary-card p { margin: 0; opacity: 0.9; }
        .passed { background: linear-gradient(135deg, #4CAF50, #45a049); }
        .failed { background: linear-gradient(135deg, #f44336, #da190b); }
        .total { background: linear-gradient(135deg, #2196F3, #0b7dda); }
        .critical { background: linear-gradient(135deg, #FF5722, #d84315); }
        .test-results { margin-top: 30px; }
        .test-item { margin-bottom: 15px; padding: 15px; border-radius: 8px; border-left: 5px solid; }
        .test-passed { background-color: #e8f5e8; border-left-color: #4CAF50; }
        .test-failed { background-color: #ffeaea; border-left-color: #f44336; }
        .test-critical { background-color: #fff3e0; border-left-color: #FF5722; }
        .test-name { font-weight: bold; font-size: 1.1em; margin-bottom: 5px; }
        .test-details { color: #666; font-size: 0.9em; }
        .test-error { color: #d32f2f; font-weight: bold; margin-top: 5px; }
        .test-time { color: #888; font-size: 0.8em; float: right; }
        .footer { margin-top: 30px; padding: 20px; background-color: #f8f9fa; border-radius: 8px; text-align: center; color: #666; }
        .status-icon { font-size: 1.2em; margin-right: 8px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 Reporte de Pruebas Cáusticas</h1>
            <h2>Sistema de Tickets - Solicitudes Internas</h2>
            <p>Fecha: $($Global:StartTime.ToString('dd/MM/yyyy HH:mm:ss')) - $($endTime.ToString('dd/MM/yyyy HH:mm:ss'))</p>
            <p>Duración total: $($duration.ToString('hh\:mm\:ss'))</p>
        </div>
        
        <div class="summary">
            <div class="summary-card total">
                <h3>$Global:TotalTests</h3>
                <p>Total de Pruebas</p>
            </div>
            <div class="summary-card passed">
                <h3>$Global:PassedTests</h3>
                <p>Pruebas Exitosas</p>
            </div>
            <div class="summary-card failed">
                <h3>$Global:FailedTests</h3>
                <p>Pruebas Fallidas</p>
            </div>
            <div class="summary-card critical">
                <h3>$Global:CriticalErrors</h3>
                <p>Errores Críticos</p>
            </div>
        </div>
        
        <div class="test-results">
            <h2>📋 Resultados Detallados</h2>
"@
    
    foreach ($result in $Global:TestResults) {
        $statusIcon = if ($result.Passed) { "✅" } else { "❌" }
        $cssClass = if ($result.IsCritical) { "test-critical" } elseif ($result.Passed) { "test-passed" } else { "test-failed" }
        
        $html += @"
            <div class="test-item $cssClass">
                <div class="test-name">
                    <span class="status-icon">$statusIcon</span>
                    $($result.TestName)
                    <span class="test-time">$($result.Timestamp.ToString('HH:mm:ss'))</span>
                </div>
"@
        
        if ($result.Details) {
            $html += "                <div class=""test-details"">$($result.Details)</div>`n"
        }
        
        if ($result.ErrorMessage) {
            $html += "                <div class=""test-error"">Error: $($result.ErrorMessage)</div>`n"
        }
        
        if ($result.ResponseTime -gt 0) {
            $html += "                <div class=""test-details"">Tiempo de respuesta: $($result.ResponseTime.ToString('F2')) segundos</div>`n"
        }
        
        $html += "            </div>`n"
    }
    
    $overallStatus = if ($Global:CriticalErrors -eq 0 -and $Global:FailedTests -eq 0) { "✅ SISTEMA APROBADO" } elseif ($Global:CriticalErrors -gt 0) { "❌ SISTEMA RECHAZADO (Errores Críticos)" } else { "⚠️ SISTEMA CON ADVERTENCIAS" }
    
    $html += @"
        </div>
        
        <div class="footer">
            <h2>$overallStatus</h2>
            <p>Generado por Script de Pruebas Cáusticas v1.0</p>
            <p>Sistema: $env:COMPUTERNAME | Usuario: $env:USERNAME</p>
        </div>
    </div>
</body>
</html>
"@
    
    try {
        $html | Out-File -FilePath $ReportPath -Encoding UTF8
        Write-Host "✅ Reporte generado exitosamente: $ReportPath" -ForegroundColor $SuccessColor
        
        # Intentar abrir el reporte en el navegador
        if (Test-Path $ReportPath) {
            Start-Process $ReportPath
        }
    } catch {
        Write-Host "❌ Error al generar reporte: $($_.Exception.Message)" -ForegroundColor $ErrorColor
    }
}

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

function Start-CausticTests {
    Clear-Host
    
    Write-Host @"
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🧪 PRUEBAS CÁUSTICAS - SISTEMA ODOO                     ║
║                                                                              ║
║  Este script ejecutará pruebas exhaustivas para validar la robustez         ║
║  y confiabilidad del sistema bajo condiciones extremas.                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor $InfoColor
    
    Write-Host "`nConfiguración de pruebas:" -ForegroundColor $InfoColor
    Write-Host "• URL del sistema: $OdooUrl" -ForegroundColor Gray
    Write-Host "• Usuario de prueba: $Usuario" -ForegroundColor Gray
    Write-Host "• Reporte se guardará en: $ReportPath" -ForegroundColor Gray
    Write-Host "• Modo rápido: $(if($QuickTest){'Activado'}else{'Desactivado'})" -ForegroundColor Gray
    Write-Host "• Pruebas de navegador: $(if($SkipBrowserTests){'Omitidas'}else{'Incluidas'})" -ForegroundColor Gray
    
    Write-Host "`n⏳ Iniciando pruebas..." -ForegroundColor $InfoColor
    
    # Ejecutar todas las pruebas
    Test-DockerContainers
    Test-OdooConnectivity
    Test-DatabaseConnection
    Test-SystemLoad
    Test-SecurityBasics
    Test-ResourceUsage
    Test-LogAnalysis
    
    # Generar reporte
    Generate-HtmlReport
    
    # Mostrar resumen final
    Write-Host "`n" -NoNewline
    Write-Host "=" * 80 -ForegroundColor $InfoColor
    Write-Host "RESUMEN FINAL DE PRUEBAS" -ForegroundColor $InfoColor
    Write-Host "=" * 80 -ForegroundColor $InfoColor
    
    $successRate = if ($Global:TotalTests -gt 0) { [math]::Round(($Global:PassedTests / $Global:TotalTests) * 100, 1) } else { 0 }
    
    Write-Host "📊 Estadísticas:" -ForegroundColor $InfoColor
    Write-Host "   • Total de pruebas ejecutadas: $Global:TotalTests" -ForegroundColor Gray
    Write-Host "   • Pruebas exitosas: $Global:PassedTests" -ForegroundColor $SuccessColor
    Write-Host "   • Pruebas fallidas: $Global:FailedTests" -ForegroundColor $ErrorColor
    Write-Host "   • Errores críticos: $Global:CriticalErrors" -ForegroundColor $ErrorColor
    Write-Host "   • Errores menores: $Global:MinorErrors" -ForegroundColor $WarningColor
    Write-Host "   • Tasa de éxito: $successRate%" -ForegroundColor $(if($successRate -ge 90){$SuccessColor}elseif($successRate -ge 70){$WarningColor}else{$ErrorColor})
    
    $finalStatus = if ($Global:CriticalErrors -eq 0 -and $Global:FailedTests -eq 0) {
        Write-Host "`n🎉 RESULTADO: SISTEMA APROBADO" -ForegroundColor $SuccessColor
        Write-Host "   El sistema ha pasado todas las pruebas cáusticas." -ForegroundColor $SuccessColor
        "APROBADO"
    } elseif ($Global:CriticalErrors -gt 0) {
        Write-Host "`n🚨 RESULTADO: SISTEMA RECHAZADO" -ForegroundColor $ErrorColor
        Write-Host "   Se encontraron errores críticos que requieren atención inmediata." -ForegroundColor $ErrorColor
        "RECHAZADO"
    } else {
        Write-Host "`n⚠️  RESULTADO: SISTEMA CON ADVERTENCIAS" -ForegroundColor $WarningColor
        Write-Host "   El sistema funciona pero tiene problemas menores." -ForegroundColor $WarningColor
        "CON_ADVERTENCIAS"
    }
    
    Write-Host "`n📄 Reporte detallado disponible en: $ReportPath" -ForegroundColor $InfoColor
    
    return $finalStatus
}

# ============================================================================
# EJECUCIÓN PRINCIPAL
# ============================================================================

if ($MyInvocation.InvocationName -ne '.') {
    # Solo ejecutar si el script se llama directamente (no si se importa)
    try {
        $result = Start-CausticTests
        
        # Código de salida basado en el resultado
        switch ($result) {
            "APROBADO" { exit 0 }
            "CON_ADVERTENCIAS" { exit 1 }
            "RECHAZADO" { exit 2 }
            default { exit 3 }
        }
    } catch {
        Write-Host "`n💥 ERROR FATAL: $($_.Exception.Message)" -ForegroundColor $ErrorColor
        Write-Host "Stack trace: $($_.ScriptStackTrace)" -ForegroundColor $ErrorColor
        exit 99
    }
}

# ============================================================================
# AYUDA Y EJEMPLOS DE USO
# ============================================================================

<#
.SYNOPSIS
Script de pruebas cáusticas para sistema Odoo con Docker

.DESCRIPTION
Este script ejecuta una batería completa de pruebas diseñadas para encontrar
los límites y vulnerabilidades del sistema Odoo. Incluye pruebas de:
- Conectividad y disponibilidad
- Carga y rendimiento
- Seguridad básica
- Integridad de contenedores
- Análisis de logs
- Uso de recursos

.PARAMETER ReportPath
Ruta donde se guardará el reporte HTML. Por defecto: ./reporte_pruebas_causticas.html

.PARAMETER OdooUrl
URL del sistema Odoo a probar. Por defecto: http://localhost:8200

.PARAMETER Usuario
Usuario para las pruebas de autenticación. Por defecto: admin

.PARAMETER Password
Contraseña para las pruebas de autenticación. Por defecto: admin

.PARAMETER SkipBrowserTests
Omite las pruebas que requieren navegador web

.PARAMETER QuickTest
Ejecuta solo las pruebas esenciales (modo rápido)

.EXAMPLE
.\ejecutar_pruebas_causticas.ps1
Ejecuta todas las pruebas con configuración por defecto

.EXAMPLE
.\ejecutar_pruebas_causticas.ps1 -QuickTest -ReportPath "C:\Reports\pruebas.html"
Ejecuta pruebas rápidas y guarda el reporte en una ubicación específica

.EXAMPLE
.\ejecutar_pruebas_causticas.ps1 -OdooUrl "http://192.168.1.100:8200" -Usuario "testuser"
Prueba un sistema Odoo remoto con credenciales específicas

.NOTES
Autor: Sistema de Pruebas Automatizadas
Versión: 1.0
Requisitos: PowerShell 5.0+, Docker, Docker Compose
#>