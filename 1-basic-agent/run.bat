@echo off
echo Installing required packages...
pip install deprecated
pip install flask flask-cors python-dotenv

echo.
echo Checking for API key...
if not exist .env (
    echo.
    echo ⚠️  ERROR: .env file not found!
    echo.
    echo Please run setup.bat first to create the .env file and add your Google API key.
    echo.
    echo Quick setup:
    echo 1. Run: setup.bat
    echo 2. Edit .env file with your Google API key
    echo 3. Get API key from: https://aistudio.google.com/app/apikey
    echo.
    pause
    exit /b 1
)

echo.
echo Starting AI News Assistant...
echo Visit http://localhost:5000 in your browser
echo.
python app.py

pause
