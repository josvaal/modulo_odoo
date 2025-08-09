# ============================================================================
# SCRIPT SIMPLE DE PRUEBAS CÁUSTICAS - VERSIÓN BÁSICA
# Para usuarios que necesitan una versión más ligera y rápida
# ============================================================================

param(
    [string]$OdooUrl = "http://localhost:8200"
)

# Colores para output
$Green = "Green"
$Red = "Red"
$Yellow = "Yellow"
$Cyan = "Cyan"

# Contadores
$TotalTests = 0
$PassedTests = 0
$FailedTests = 0

function Test-Simple {
    param(
        [string]$TestName,
        [scriptblock]$TestCode,
        [bool]$IsCritical = $false
    )
    
    $global:TotalTests++
    Write-Host "`n🧪 Ejecutando: $TestName" -ForegroundColor $Cyan
    
    try {
        $result = & $TestCode
        if ($result) {
            $global:PassedTests++
            Write-Host "✅ PASÓ: $TestName" -ForegroundColor $Green
        } else {
            $global:FailedTests++
            Write-Host "❌ FALLÓ: $TestName" -ForegroundColor $Red
            if ($IsCritical) {
                Write-Host "⚠️  CRÍTICO: Este error puede afectar el funcionamiento del sistema" -ForegroundColor $Yellow
            }
        }
        return $result
    } catch {
        $global:FailedTests++
        Write-Host "❌ ERROR en $TestName`: $($_.Exception.Message)" -ForegroundColor $Red
        return $false
    }
}

# ============================================================================
# PRUEBAS PRINCIPALES
# ============================================================================

Clear-Host
Write-Host @"
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🧪 PRUEBAS CÁUSTICAS SIMPLES                            ║
║                         Sistema Odoo - Versión Rápida                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor $Cyan

Write-Host "`nURL del sistema: $OdooUrl`n" -ForegroundColor $Cyan

# Prueba 1: Verificar contenedores Docker
Test-Simple "Contenedores Docker" {
    $containers = docker-compose ps -q
    $runningContainers = docker-compose ps --filter "status=running" -q
    return $containers.Count -eq $runningContainers.Count -and $containers.Count -gt 0
} -IsCritical $true

# Prueba 2: Conectividad HTTP
Test-Simple "Conectividad HTTP" {
    try {
        $response = Invoke-WebRequest -Uri $OdooUrl -UseBasicParsing -TimeoutSec 10
        return $response.StatusCode -eq 200
    } catch {
        return $false
    }
} -IsCritical $true

# Prueba 3: Base de datos PostgreSQL
Test-Simple "Base de Datos PostgreSQL" {
    try {
        $dbCheck = docker exec modulo_odoo-db-1 pg_isready -U odoo 2>$null
        return $LASTEXITCODE -eq 0
    } catch {
        return $false
    }
} -IsCritical $true

# Prueba 4: Tiempo de respuesta
Test-Simple "Tiempo de Respuesta" {
    try {
        $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
        $response = Invoke-WebRequest -Uri $OdooUrl -UseBasicParsing -TimeoutSec 15
        $stopwatch.Stop()
        $responseTime = $stopwatch.Elapsed.TotalSeconds
        Write-Host "   Tiempo: $($responseTime.ToString('F2')) segundos" -ForegroundColor Gray
        return $responseTime -lt 5.0
    } catch {
        return $false
    }
}

# Prueba 5: Logs de errores
Test-Simple "Análisis de Logs" {
    try {
        $logs = docker-compose logs --tail=20 odoo 2>$null
        if ($logs) {
            $errors = $logs | Select-String -Pattern "ERROR|CRITICAL|FATAL"
            Write-Host "   Errores encontrados: $($errors.Count)" -ForegroundColor Gray
            return $errors.Count -eq 0
        }
        return $false
    } catch {
        return $false
    }
}

# Prueba 6: Uso de memoria
Test-Simple "Uso de Recursos" {
    try {
        $stats = docker stats --no-stream --format "{{.MemPerc}}" 2>$null
        if ($stats) {
            Write-Host "   Estadísticas de memoria obtenidas" -ForegroundColor Gray
            return $true
        }
        return $false
    } catch {
        return $false
    }
}

# Prueba 7: Múltiples requests
Test-Simple "Carga Básica (5 requests)" {
    try {
        $successCount = 0
        for ($i = 1; $i -le 5; $i++) {
            try {
                $response = Invoke-WebRequest -Uri $OdooUrl -UseBasicParsing -TimeoutSec 8
                if ($response.StatusCode -eq 200) { $successCount++ }
            } catch { }
        }
        Write-Host "   Requests exitosos: $successCount/5" -ForegroundColor Gray
        return $successCount -ge 4
    } catch {
        return $false
    }
}

# ============================================================================
# RESUMEN FINAL
# ============================================================================

Write-Host "`n" + "=" * 80 -ForegroundColor $Cyan
Write-Host "RESUMEN DE PRUEBAS" -ForegroundColor $Cyan
Write-Host "=" * 80 -ForegroundColor $Cyan

$successRate = if ($TotalTests -gt 0) { [math]::Round(($PassedTests / $TotalTests) * 100, 1) } else { 0 }

Write-Host "📊 Resultados:" -ForegroundColor $Cyan
Write-Host "   • Total de pruebas: $TotalTests" -ForegroundColor Gray
Write-Host "   • Exitosas: $PassedTests" -ForegroundColor $Green
Write-Host "   • Fallidas: $FailedTests" -ForegroundColor $Red
Write-Host "   • Tasa de éxito: $successRate%" -ForegroundColor $(if($successRate -ge 85){$Green}elseif($successRate -ge 70){$Yellow}else{$Red})

# Determinar estado final
if ($FailedTests -eq 0) {
    Write-Host "`n🎉 RESULTADO: SISTEMA FUNCIONANDO CORRECTAMENTE" -ForegroundColor $Green
    Write-Host "   Todas las pruebas básicas han sido exitosas." -ForegroundColor $Green
    $exitCode = 0
} elseif ($successRate -ge 70) {
    Write-Host "`n⚠️  RESULTADO: SISTEMA FUNCIONAL CON ADVERTENCIAS" -ForegroundColor $Yellow
    Write-Host "   La mayoría de pruebas pasaron, pero hay algunos problemas menores." -ForegroundColor $Yellow
    $exitCode = 1
} else {
    Write-Host "`n🚨 RESULTADO: SISTEMA CON PROBLEMAS SIGNIFICATIVOS" -ForegroundColor $Red
    Write-Host "   Se requiere atención inmediata para resolver los problemas encontrados." -ForegroundColor $Red
    $exitCode = 2
}

Write-Host "`n💡 Para pruebas más detalladas, ejecuta: .\ejecutar_pruebas_causticas.ps1" -ForegroundColor $Cyan
Write-Host "⏱️  Tiempo total: $((Get-Date) - $startTime | ForEach-Object {$_.ToString('mm\:ss')}) minutos" -ForegroundColor Gray

# Generar reporte simple en texto
$reportFile = "reporte_simple_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
$report = @"
REPORTE SIMPLE DE PRUEBAS CÁUSTICAS
====================================
Fecha: $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')
Sistema: $OdooUrl

RESULTADOS:
- Total de pruebas: $TotalTests
- Exitosas: $PassedTests
- Fallidas: $FailedTests
- Tasa de éxito: $successRate%

ESTADO FINAL: $(if($exitCode -eq 0){'FUNCIONANDO CORRECTAMENTE'}elseif($exitCode -eq 1){'FUNCIONAL CON ADVERTENCIAS'}else{'CON PROBLEMAS SIGNIFICATIVOS'})

Generado por: $env:USERNAME en $env:COMPUTERNAME
"@

try {
    $report | Out-File -FilePath $reportFile -Encoding UTF8
    Write-Host "`n📄 Reporte simple guardado en: $reportFile" -ForegroundColor $Cyan
} catch {
    Write-Host "`n⚠️  No se pudo guardar el reporte: $($_.Exception.Message)" -ForegroundColor $Yellow
}

exit $exitCode