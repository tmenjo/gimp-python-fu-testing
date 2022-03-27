@echo off
rem SPDX-License-Identifier: MIT
rem Copyright (c) 2022 Takashi Menjo

setlocal
pushd "%~dp0%\.."

set python_exe=python.exe

rem "Install for me only"
set "local_python_home=%LOCALAPPDATA%\Programs\GIMP 2"
set "local_python=%local_python_home%\bin\%python_exe%"
set "local_python_extra_lib=%local_python_home%\lib\gimp\2.0\python"
rem "Install for all users"
set "global_python_home=%ProgramFiles%\GIMP 2"
set "global_python=%global_python_home%\bin\%python_exe%"
set "global_python_extra_lib=%global_python_home%\lib\gimp\2.0\python"

if exist "%local_python%" (
	set "python=%local_python%"
	set "python_extra_lib=%local_python_extra_lib%"
) else if exist "%global_python%" (
	set "python=%global_python%"
	set "python_extra_lib=%global_python_extra_lib%"
) else (
	echo %python_exe% not found
	goto :finally
)

@echo on

set "PYTHONPATH=%python_extra_lib%"
"%python%" test_shrink.py

@echo off

del /Q *.pyc

:finally
echo.
pause
exit /b
