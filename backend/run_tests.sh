#!/usr/bin/env bash
# Ejecuta la suite de pruebas automatizadas del backend CMEDriver.
# Uso:
#   ./run_tests.sh                 # corre todas las pruebas
#   ./run_tests.sh services        # corre solo las pruebas del app "services"
#   ./run_tests.sh services.tests.NovedadTests   # corre solo una clase de pruebas

set -e
cd "$(dirname "$0")"

if [ -f ".venv/Scripts/python.exe" ]; then
    PYTHON=".venv/Scripts/python.exe"   # Windows venv layout
elif [ -f ".venv/bin/python" ]; then
    PYTHON=".venv/bin/python"           # macOS/Linux venv layout
else
    echo "No se encontro el entorno virtual (.venv). Crealo primero con: python3 -m venv .venv"
    exit 1
fi

if [ -z "$1" ]; then
    "$PYTHON" manage.py test -v 2
else
    "$PYTHON" manage.py test "$1" -v 2
fi
