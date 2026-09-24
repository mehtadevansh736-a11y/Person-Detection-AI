@echo off
REM Person Detection launcher - D:\PersonDetection
REM Usage: run_person_detection.bat <image/video/webcam-index> [model: n^|s^|m]  (default model: s)
D:\PersonDetection\venv\python.exe D:\PersonDetection\detect_person.py %*
pause
