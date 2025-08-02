@echo off
echo ============================================
echo 🎹 Piano Technique Master - Starting...
echo ============================================
echo.

echo Installing dependencies...
pip install -r requirements.txt
cd backend
pip install -r requirements.txt
cd ..

echo.
echo Starting backend server...
echo Open http://localhost:5000 in your browser
echo Then open frontend/index.html
echo.
echo Press Ctrl+C to stop the server
echo.

cd backend
python app.py
