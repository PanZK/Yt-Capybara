# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['../Yt-Capybara.py'],
    pathex=[],
    binaries=[],
    datas=[('../icons','icons')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['cryptography','lib-dynload','numpy','libcrypto','libcrypto.1.1','QtDBus','libncursesw','libncursesw.5','libssl','libssl.1.1','QtSvg'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Yt-Capybara',
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
    contents_directory='.',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Yt-Capybara',
)
