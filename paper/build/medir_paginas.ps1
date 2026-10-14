# Mide con Word (COM) el numero de paginas por seccion de un .docx, sin modificarlo.
# Uso:  powershell -File medir_paginas.ps1 -Ruta ..\Proyecto_CMEDriver_Unificado.docx
param([Parameter(Mandatory = $true)][string]$Ruta)

$origen = (Resolve-Path $Ruta).Path
$copia = Join-Path $env:TEMP ('medir_' + [guid]::NewGuid().ToString('N') + '.docx')
Copy-Item $origen $copia -Force
$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.DisplayAlerts = 0
try {
    $d = $w.Documents.Open($copia, $false, $true)
    $d.Repaginate()
    $n = $d.Paragraphs.Count
    $secciones = @()
    for ($i = 1; $i -le $n; $i++) {
        $p = $d.Paragraphs.Item($i)
        if ($p.OutlineLevel -eq 1) {
            $secciones += [pscustomobject]@{ Titulo = $p.Range.Text.Trim(); Indice = $i; Inicio = $p.Range.Information(3) }
        }
    }
    "Paginas totales: " + $d.ComputeStatistics(2)
    for ($s = 0; $s -lt $secciones.Count; $s++) {
        $fin = if ($s + 1 -lt $secciones.Count) { $secciones[$s + 1].Indice - 1 } else { $n }
        # ultimo parrafo con texto de la seccion
        $k = $fin
        while ($k -gt $secciones[$s].Indice -and $d.Paragraphs.Item($k).Range.Text.Trim().Length -eq 0) { $k-- }
        $r = $d.Paragraphs.Item($k).Range
        $r.Collapse(0)   # al final del rango
        $r.MoveEnd(1, -1) | Out-Null
        $pagFin = $d.Paragraphs.Item($k).Range.Information(3)
        # posicion vertical del final del ultimo parrafo (puntos desde el borde superior; area util 72 a 720)
        $rr = $d.Paragraphs.Item($k).Range
        $rr.SetRange($rr.End - 1, $rr.End - 1)
        $y = $rr.Information(6)
        $uso = [Math]::Round(($y - 72) / 648 * 100)
        $paginas = ($pagFin - $secciones[$s].Inicio) + 1
        $texto = $d.Range($d.Paragraphs.Item($secciones[$s].Indice).Range.Start, $d.Paragraphs.Item($fin).Range.End).ComputeStatistics(0)
        "{0,-22} paginas {1}-{2} ({3} pag.)  ultima pagina usada al {4}%  palabras {5}" -f $secciones[$s].Titulo, $secciones[$s].Inicio, $pagFin, $paginas, $uso, $texto
    }
    $d.Close($false)
}
finally {
    $w.Quit()
    Start-Sleep -Milliseconds 800
    try { Remove-Item -LiteralPath $copia -Force -ErrorAction Stop } catch { }
    Get-Process WINWORD -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -eq '' } | Stop-Process -Force -ErrorAction SilentlyContinue
}
