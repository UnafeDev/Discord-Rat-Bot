# Discord-Rat-Bot
A easy to use remote acess tool controlled via a discord server!

# Disclaimer

This tool/script is provided for educational purposes only and is made with purely educational intent. 
I am not responsible for any damages or consequences that may come from its use. 

I take no part in, nor do I endorse, any activities you choose to perform or add with this tool.

# Note
There will not be any releases as when compiled, it will automatically use the inputted token; Not yours.

IF THE JOINMIC COMMAND DOESNT WORK WHILE TESTING TRY RUNNING THIS IN CMD AND RECOMPILE :
pip install "discord.py[voice] @ git+https://github.com/rapptz/discord.py"

# Usage 

This is a script that when run on the host, will send a connected message in the discord channel (change the ID and token within the script)

To elaborate:
- the script is simply hosted on the machine, and will listen for commands using a discord server
- the server will require at least *1 text channel* and *1 voice channel*

Command prefix is (!)

|Command|Description|Example|
|-|-|-|
|!ss| Take a screenshot|
|!ip| Get public IP address|
|!web| Take a webcam photo|
|!log| Start keystroke logging|
|!slog| Stop keystroke logging and send log|
|!listf| List files in a directory (default is current directory)|
|!shutdown| Shutdown the computer|
|!cmd [command]| Execute a shell command|!cmd notepad|
|!stream| Start streaming the screen|
|!stopstream| Stop the current screen stream|
|!hardware| Get detailed hardware information|
|!cmdlist| List available commands|
|!autostart| Add this script to Windows startup|
|!upload| Upload files from Discord to the machine|!upload *attachment*
|!ps [command]| Run a PowerShell command silently|!ps notepad
|!joinmic| Join a voice channel and stream mic input|
|!stopmic| Stop mic streaming|
|!control move [x] [y]| Move mouse to (x, y)|!control move 100 100
|!control click [left/right/middle]| Click mouse button| !control click right
|!control type [text]| Type out text| !control type i see you
|!control press [key]| Press a single key| !control press 1
|!control hold [key]| Hold down a key (use !control release to release it)|!control hold 1
|!control release [key]| Release a held key|!control release 1
|!clipboard| View clipboard content|
|!clipboard set [text]| Set clipboard content|!clipboard hello there
|!clipboard clear| Clear clipboard content|
|!proclist| List running processes|
|!prockill [pid_or_process_name]| Kill a process by PID or name|!prockill discord.exe
|!systeminfo| Show system info that updates every 10 seconds|
|!tts [text]| Text-to-speech command to speak text aloud|!tts hello there
|!mouse_prank [duration] [interval] [distance]| Shake or randomly move the mouse for a duration|!mouse prank 10 0.005 100
|!specialkeylist| List special keys for use in macros|
|!keymacro [macro_script]| Execute a key macro script (e.g. {enter}, {ctrl+a})|!keymacro this will send a message {enter}
|!volume [level]| Adjust system master volume (0-100)|!volume 34
|!brightness [level]| Adjust screen brightness (0-100)|!brightness 65
|!cpu_stress [duration]| Stress CPU for a duration in seconds|!cpu_stress 15
|!getipconfig| Get IP configuration details|
|!vpnstatus| Check VPN status|
|!setcursor [url/image]| Change cursor's image|Untested.
|!draw [shape] [coordinates]| Draw shapes on the screen|!draw circle 500 500
|!draw text [x,y][text]| Draw text on the screen|!draw text 1000 1000 hello
|!rotate [degrees]| Rotate the screen by specified degrees|!rotate [0, 90, 180, 270]
|!wallpaper [url/image]| Change desktop wallpaper|!wallpaper https://image.url
|!wifi_passwords| Get saved Wi-Fi passwords|
|!lockpc| Lock the Windows session immediately|

# Step 1
Change these IDs to your channel IDs.

![screenshot](https://github.com/UnafeDev/Discord-Rat-Bot/blob/main/Imgs/editme2.png)

# Step 2
Scroll to the very bottom of the script and change the string value to your bot token.

![screenshot](https://github.com/UnafeDev/Discord-Rat-Bot/blob/main/Imgs/token.png)

# How do i get a bot token?

to get a bot token you must go to the discord developer portal : https://discord.com/developers/applications

Create a new application and name it whatever you'd like, then make your way over to OAuth2 where you can copy your bot token
- BEFORE THE BOT CAN WORK YOU MUST GO TO THE "Bot" PAGE, ENABLE ALL INTENTS AS SUCH :

![screenshot](https://github.com/UnafeDev/Discord-Rat-Bot/blob/main/Imgs/gatewaus.png)

after you do that, you need to return to tha OAuth page and set a redirect uri :
![screenshot](https://github.com/UnafeDev/Discord-Rat-Bot/blob/main/Imgs/uri.png)
- Change the "port" to a 5 digit port number

before copying the link at the bottom, select the following options (for it to be able to join and listen for commands)
![screenshot](https://github.com/UnafeDev/Discord-Rat-Bot/blob/main/Imgs/uri2.png)

# Final stretch!

Before using the file anywhere, I would reccomend renaming it to something more inconspicuous

# How universal is it?

Not quite to be blunt.

The script is made to only work on windows, but I may work on something like a linux port, stay tuned to see!


# Compiling
Assuming you already have the imports run this command where the script is (Rat.py)

pyinstaller --additional-hooks-dir . --noconsole --onefile --add-binary "ffmpeg.exe;." --add-binary "libopus-0.dll;." --icon=incon.ico rat.py

- the "--icon=incon.ico" is optional if you dont have a provided icon.

## If you dont have any of the dependencies, run this in your command prompt :
pip install discord.py pyautogui opencv-python requests psutil pynput numpy mss sounddevice pyperclip pillow imageio-ffmpeg pyttsx3 pycaw screen-brightness-control setproctitle certifi pywin32 comtypes
