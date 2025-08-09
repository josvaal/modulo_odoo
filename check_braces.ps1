# Script para verificar llaves de funciones
$content = Get-Content 'ejecutar_pruebas_causticas.ps1'
$functions = @()
$currentFunction = $null
$braceCount = 0

for ($i = 0; $i -lt $content.Length; $i++) {
    $line = $content[$i]
    
    if ($line -match '^function\s+(\w+)\s*\{') {
        if ($currentFunction) {
            $functions += [PSCustomObject]@{
                Name = $currentFunction
                StartLine = $startLine
                EndLine = $i
                BraceBalance = $braceCount
            }
        }
        $currentFunction = $matches[1]
        $startLine = $i + 1
        $braceCount = 1
    }
    elseif ($currentFunction) {
        $openBraces = ($line | Select-String -Pattern '\{' -AllMatches).Matches.Count
        $closeBraces = ($line | Select-String -Pattern '\}' -AllMatches).Matches.Count
        $braceCount += $openBraces - $closeBraces
        
        if ($braceCount -eq 0) {
            $functions += [PSCustomObject]@{
                Name = $currentFunction
                StartLine = $startLine
                EndLine = $i + 1
                BraceBalance = 0
            }
            $currentFunction = $null
        }
    }
}

# Si queda una función sin cerrar
if ($currentFunction) {
    $functions += [PSCustomObject]@{
        Name = $currentFunction
        StartLine = $startLine
        EndLine = "NO CERRADA"
        BraceBalance = $braceCount
    }
}

$functions | Format-Table -AutoSize