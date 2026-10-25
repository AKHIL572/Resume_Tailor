# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from pathlib import Path

block_cipher = None

root_dir = Path(os.path.abspath(SPECPATH)).parent

# Data files to bundle with the binary:
# - prompts/ (all 7 rule files)
# - templates/ (LaTeX templates)
# - assets/ (icons)
# - master_profile.md (default profile)
datas = [
    (str(root_dir / 'prompts'), 'prompts'),
    (str(root_dir / 'templates'), 'templates'),
    (str(root_dir / 'assets'), 'assets'),
]

if (root_dir / 'master_profile.md').exists():
    datas.append((str(root_dir / 'master_profile.md'), '.'))

if (root_dir / 'bin').exists():
    datas.append((str(root_dir / 'bin'), 'bin'))

icon_path = str(root_dir / 'assets' / 'icon.ico')
if not os.path.exists(icon_path):
    icon_path = None

a = Analysis(
    [str(root_dir / 'app' / 'main.py')],
    pathex=[str(root_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'pydantic',
        'keyring',
        'keyring.backends',
        'platformdirs',
        'fitz',
        'PySide6',
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'openai',
        'httpx',
        'json_repair',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'numpy', 'scipy'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='JobTailor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)
