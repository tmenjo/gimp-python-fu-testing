@echo off
rem SPDX-License-Identifier: MIT
rem Copyright (c) 2022 Takashi Menjo

setlocal
pushd "%~dp0"

set gimp_exe=gimp-2.10.exe

set "local_gimp=%LOCALAPPDATA%\Programs\GIMP 2\bin\%gimp_exe%"
set "global_gimp=%ProgramFiles%\GIMP 2\bin\%gimp_exe%"

if exist "%local_gimp%" (
	set "gimp=%local_gimp%"
) else if exist "%global_gimp%" (
	set "gimp=%global_gimp%"
) else (
	echo %gimp_exe% not found
	goto :finally
)

set LANG=C

@echo on

"%gimp%" -i -d -f --batch-interpreter python-fu-eval ^
	-b - -b "pdb.gimp_quit(1)" < dump_sys_argv.py

@echo off

:finally
echo.
pause
exit /b
