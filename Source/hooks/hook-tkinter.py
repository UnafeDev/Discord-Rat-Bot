from PyInstaller.utils.hooks import collect_all
import os
import tkinter

def find_tk_data_directory():
    # Find the Tkinter data directory dynamically
    tk_root = tkinter.Tk()
    tk_root.withdraw()  # Hide the root window
    tk_data_dir = os.path.dirname(tkinter.__file__)
    tk_root.destroy()  # Destroy the root window
    return tk_data_dir

datas, binaries, hiddenimports = collect_all('tkinter')

# Dynamically find the Tk data directory and include it
tk_data_dir = find_tk_data_directory()
datas.append((tk_data_dir, 'tk_data'))

# Additional hidden imports for Tkinter
hiddenimports.extend(['tkinter.ttk', 'tkinter.font', 'tkinter.colorchooser', 'tkinter.messagebox', 'tkinter.simpledialog'])