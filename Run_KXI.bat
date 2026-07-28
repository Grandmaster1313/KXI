@echo off
title KXI Gold Command Center

cd /d C:\Users\herna\OneDrive\Documents\KXI\GoldCommandCenter

call ..\venv312\Scripts\activate.bat

python scheduler.py

pause