from PyInstaller.utils.hooks import copy_metadata, collect_data_files

# Collect package metadata (helps with version info, etc.)
datas = copy_metadata('win10toast')

# Collect data files if any (like icons, manifests, etc.)
datas += collect_data_files('win10toast')

# If win10toast depends on any hidden imports, list them here:
hiddenimports = []