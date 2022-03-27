@echo off
rem SPDX-License-Identifier: MIT
rem Copyright (c) 2022 Takashi Menjo

setlocal
pushd "%~dp0%\.."

set python_exe=python.exe

rem "Install for me only"
set "local_python_home=%LOCALAPPDATA%\Programs\GIMP 2"
set "local_python=%local_python_home%\bin\%python_exe%"
rem "Install for all users"
set "global_python_home=%ProgramFiles%\GIMP 2"
set "global_python=%global_python_home%\bin\%python_exe%"

if exist "%local_python%" (
	set "python=%local_python%"
) else if exist "%global_python%" (
	set "python=%global_python%"
) else (
	echo %python_exe% not found
	goto :finally
)

@echo on

"%python%" test_shrink.py

@echo off

:finally
echo.
pause
exit /b
