# Script para probar sintaxis
try {
    $content = Get-Content 'ejecutar_pruebas_causticas.ps1' -Raw
    $scriptBlock = [ScriptBlock]::Create($content)
    Write-Host "Sintaxis válida" -ForegroundColor Green
} catch {
    Write-Host "Error de sintaxis: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Línea: $($_.InvocationInfo.ScriptLineNumber)" -ForegroundColor Yellow
}