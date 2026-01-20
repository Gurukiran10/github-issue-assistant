"""
Development and run scripts
"""

# Backend startup script
@echo off
echo Starting GitHub Issue Assistant...
echo.
echo [1/2] Installing dependencies...
pip install -r requirements.txt

echo.
echo [2/2] Starting backend API (http://localhost:8000)...
cd backend
python main.py
