#!/bin/bash
# Backend startup script for macOS/Linux

echo "Starting GitHub Issue Assistant Backend..."
echo ""
echo "[1/2] Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "[2/2] Starting backend API (http://localhost:8000)..."
cd backend
python main.py
