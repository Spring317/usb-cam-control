# -*- mode: python ; coding: utf-8 -*-
import sys
import os

block_cipher = None

extra_binaries = []
extra_datas = []

from PyInstaller.utils.hooks import collect_all
import importlib.util

# The PyPI gphoto2 wheel bundles its own libgphoto2 plus camlibs/iolibs.
# Collect all of it so the app uses one consistent set of libraries.
_gp_dir = os.path.dirname(importlib.util.find_spec('gphoto2').origin)
gphoto2_wheel_bundled = os.path.isdir(os.path.join(_gp_dir, 'camlibs'))
extra_hiddenimports = []
if gphoto2_wheel_bundled:
    _datas, _binaries, _hidden = collect_all('gphoto2')
    extra_datas += _datas
    extra_binaries += _binaries
    extra_hiddenimports += _hidden

# Otherwise (gphoto2 built from source) fall back to Homebrew's libgphoto2
if sys.platform == 'darwin' and not gphoto2_wheel_bundled:
    # Default brew prefix on Apple Silicon is /opt/homebrew, on Intel is /usr/local
    brew_prefixes = ['/opt/homebrew', '/usr/local']
    for prefix in brew_prefixes:
        if os.path.exists(prefix + '/lib/libgphoto2.dylib'):
            extra_binaries += [
                (prefix + '/lib/libgphoto2.dylib', '.'),
                (prefix + '/lib/libgphoto2_port.dylib', '.'),
            ]
            extra_datas += [
                (prefix + '/lib/libgphoto2', 'libgphoto2'),
                (prefix + '/lib/libgphoto2_port', 'libgphoto2_port'),
            ]
            break

a = Analysis(
    ['desktop_app.py'],
    pathex=['backend'],
    binaries=extra_binaries,
    datas=[
        ('frontend', 'frontend'),
        *extra_datas,
    ],
    hiddenimports=[
        'uvicorn.logging',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
        'webview',
        'camera_controller',
        *extra_hiddenimports,
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='CanonControl',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='CanonControl',
)
app = BUNDLE(
    coll,
    name='CanonControl.app',
    icon=None,
    bundle_identifier='com.spring317.canoncontrol',
)
