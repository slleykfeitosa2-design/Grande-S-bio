@echo off
cd /d E:\GrandeSabio
pip install google-genai
pip install colorama
setx GEMINI_API_KEY "Sua Chave aqui"
python grande_sabio.py
pause
