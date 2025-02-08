# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_dynamic_libs
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.utils.hooks import collect_all

datas = [('C:\\Github\\crud-catastrov2\\config\\config.json', '.'), ('C:\\Github\\crud-catastrov2\\config', 'config/'), ('C:\\Github\\crud-catastrov2\\modulos\\c.json', '.')]
binaries = []
hiddenimports = []
datas += collect_data_files('tkcalendar')
datas += collect_data_files('babel')
binaries += collect_dynamic_libs('tkcalendar')
binaries += collect_dynamic_libs('babel')
hiddenimports += collect_submodules('tkcalendar')
hiddenimports += collect_submodules('babel')
tmp_ret = collect_all('tkcalendar')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('babel')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['C:\\Github\\crud-catastrov2\\main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=['C:\\Github\\crud-catastrov2\\hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Axio',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Github\\crud-catastrov2\\assets\\axiow.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Axio',
)
