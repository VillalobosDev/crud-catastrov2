# hook-tkcalendar.py
from PyInstaller.utils.hooks import collect_submodules

# Incluye todos los submódulos de tkcalendar
hiddenimports = collect_submodules('tkcalendar')
