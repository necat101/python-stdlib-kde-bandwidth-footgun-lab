@echo off
setlocal
REM interpreter discovery: %PYTHON_BIN%, python3.14, python3.13, python3, python
if defined PYTHON_BIN (
  set PY=%PYTHON_BIN%
  goto run
)
where python3.14 >nul 2>nul && set PY=python3.14 && goto run
where python3.13 >nul 2>nul && set PY=python3.13 && goto run
where python3 >nul 2>nul && set PY=python3 && goto run
set PY=python
:run
echo using %PY%
%PY% -m py_compile run_lab.py test_lab.py || exit /b %ERRORLEVEL%
%PY% run_lab.py || exit /b %ERRORLEVEL%
%PY% -m unittest -v || exit /b %ERRORLEVEL%
