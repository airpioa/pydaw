@echo off
REM Set the installer and uninstaller Python script paths
SET INSTALLER_SCRIPT=installer.py
SET UNINSTALLER_SCRIPT=uninstaller.py

REM Set the output directory
SET OUTPUT_DIR=dist

REM Clean up old build directories
CALL :clean

REM Check if PyInstaller is installed
CALL :check_pyinstaller

REM Build the installer and uninstaller
CALL :build_app "%INSTALLER_SCRIPT%" "PyDAW_Installer.exe"
CALL :build_app "%UNINSTALLER_SCRIPT%" "PyDAW_Uninstaller.exe"

echo Build complete!

REM End of the script
goto :eof

REM Function to clean up old build directories
:clean
echo Cleaning up old builds...
rmdir /s /q build
rmdir /s /q dist
del /f /q *.spec
goto :eof

REM Function to check if PyInstaller is installed
:check_pyinstaller
echo Checking if PyInstaller is installed...
python -m pyinstaller --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo PyInstaller is not installed. Installing it now...
    pip install pyinstaller
)
goto :eof

REM Function to build the app using PyInstaller
:build_app
SET SCRIPT_NAME=%1
SET OUTPUT_NAME=%2

echo Building %OUTPUT_NAME%...

pyinstaller --onefile --windowed --add-data "icon.png;." "%SCRIPT_NAME%"

REM Move the built app to the desired output directory
move /y "dist\%SCRIPT_NAME%" "%OUTPUT_DIR%\%OUTPUT_NAME%"

echo %OUTPUT_NAME% built and moved to %OUTPUT_DIR%.
goto :eof
