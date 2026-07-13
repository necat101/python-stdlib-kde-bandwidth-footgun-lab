#!/usr/bin/env sh
set -eu
# interpreter discovery: $PYTHON_BIN, python3.14, python3.13, python3, python
if [ -n "${PYTHON_BIN:-}" ] && command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  PY="$PYTHON_BIN"
elif command -v python3.14 >/dev/null 2>&1; then
  PY=python3.14
elif command -v python3.13 >/dev/null 2>&1; then
  PY=python3.13
elif command -v python3 >/dev/null 2>&1; then
  PY=python3
else
  PY=python
fi
echo "using $PY"
"$PY" -m py_compile run_lab.py test_lab.py
"$PY" run_lab.py
"$PY" -m unittest -v
