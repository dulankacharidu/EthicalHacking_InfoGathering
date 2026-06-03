@echo off
echo =====================================
echo ⚠️  InfoHub Toolkit  ⚠️
echo!~  Developed by Dulanka Charidu  ~
echo =====================================
echo =====================================
echo Information Gathering Techniques
echo Viewer for Ethical Hacking Course
echo =====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.7+ from https://python.org
    echo Then run: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo Checking dependencies...
pip show colorama >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required packages...
    pip install colorama
)

echo.
echo Running Information Gathering Techniques Viewer...
echo.
python tools/info_viewer.py %*

echo.
pause
