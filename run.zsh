#!/usr/bin/env zsh
set -eu
# interpreter discovery: $PYTHON_BIN, python3.14, python3.13, python3, python
if [[ -n "${PYTHON_BIN:-}" ]] && (( $+commands[$PYTHON_BIN] )); then
  PY="$PYTHON_BIN"
elif (( $+commands[python3.14] )); then
  PY=python3.14
elif (( $+commands[python3.13] )); then
  PY=python3.13
elif (( $+commands[python3] )); then
  PY=python3
else
  PY=python
fi
echo "using $PY"
"$PY" -m py_compile run_lab.py test_lab.py
"$PY" run_lab.py
"$PY" -m unittest -v
