#!/bin/bash
# Frontend startup script for macOS/Linux

echo "Starting GitHub Issue Assistant Frontend..."
echo ""
echo "[1/2] Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "[2/2] Starting Streamlit UI (http://localhost:8501)..."
cd frontend
streamlit run app.py
