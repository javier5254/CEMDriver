# Ejecuta la suite de pruebas automatizadas del backend CMEDriver.
# Uso:
#   ./run_tests.ps1                a corre todas las pruebas
#   ./run_tests.ps1 services       a corre solo las pruebas del app "services"
#   ./run_tests.ps1 services.tests.NovedadTests   a corre solo una clase de pruebas

param(
    [string]$Target = ""
)

$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $python)) {
    Write-Host "No se encontro el entorno virtual (.venv). Crealo primero con: py -m venv .venv" -ForegroundColor Red
    exit 1
}

if ($Target -eq "") {
    & $python manage.py test -v 2
} else {
    & $python manage.py test $Target -v 2
}
