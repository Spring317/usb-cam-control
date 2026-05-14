# -*- mode: python ; coding: utf-8 -*-
import sys
import os

block_cipher = None

a = Analysis(
    ['desktop_app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('frontend', 'frontend')
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
        'webview'
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

# On macOS, include homebrew libgphoto2 dependencies
if sys.platform == 'darwin':
    # Default brew prefix on Apple Silicon is /opt/homebrew, on Intel is /usr/local
    brew_prefixes = ['/opt/homebrew', '/usr/local']
    for prefix in brew_prefixes:
        if os.path.exists(prefix + '/lib/libgphoto2.dylib'):
            a.binaries += [
                (prefix + '/lib/libgphoto2.dylib', '.'),
                (prefix + '/lib/libgphoto2_port.dylib', '.'),
            ]
            a.datas += [
                (prefix + '/lib/libgphoto2', 'libgphoto2'),
                (prefix + '/lib/libgphoto2_port', 'libgphoto2_port')
            ]
            break

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
