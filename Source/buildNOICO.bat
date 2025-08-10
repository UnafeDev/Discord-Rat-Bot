cd /d "%~dp0"
pyinstaller --onefile --add-binary "ffmpeg.exe;." --add-binary "libopus-0.dll;." --hidden-import aiohttp --additional-hooks-dir . --hidden-import certifi rat.py
