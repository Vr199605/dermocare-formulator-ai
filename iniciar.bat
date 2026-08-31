@echo off
title Dermocare Formulator AI
echo ======================================================
echo    Iniciando Dermocare Formulator AI (Streamlit)...
echo ======================================================
cd /d "%~dp0"
python -m streamlit run streamlit_app.py
pause
