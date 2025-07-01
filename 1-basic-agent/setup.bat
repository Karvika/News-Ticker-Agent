@echo off
echo Setting up AI News Assistant Web Interface...
echo.

echo Step 1: Installing missing dependency 'deprecated'...
pip install deprecated

echo.
echo Step 2: Installing web interface dependencies...
pip install flask flask-cors python-dotenv

echo.
echo Step 3: Setting up environment file...
if not exist .env (
    if exist .env.example (
        copy .env.example .env
        echo Created .env file from .env.example
        echo.
        echo ⚠️  IMPORTANT: Edit .env file and add your Google API key!
        echo    1. Get your API key from: https://aistudio.google.com/app/apikey
        echo    2. Open .env file in notepad
        echo    3. Replace 'your_google_api_key_here' with your actual API key
        echo.
    ) else (
        echo GOOGLE_API_KEY=your_google_api_key_here > .env
        echo Created .env file
        echo.
        echo ⚠️  IMPORTANT: Edit .env file and add your Google API key!
        echo    1. Get your API key from: https://aistudio.google.com/app/apikey
        echo    2. Open .env file in notepad
        echo    3. Replace 'your_google_api_key_here' with your actual API key
        echo.
    )
) else (
    echo .env file already exists
)

echo.
echo Setup complete! 
echo.
echo ⚠️  BEFORE RUNNING: Make sure to add your Google API key to the .env file
echo 📝 Get your API key from: https://aistudio.google.com/app/apikey
echo.
echo You can now run the application with:
echo   python app.py
echo.
echo Or use the run.bat file for a one-click start.
pause
