"""
Used for MSI file generation using `cx_Freeze` package.

This File has no relations to actual program logic. This is an independent file only
used for creating windows executable packaged in a Microsoft Installer (msi).
Program build and tested only in 64bit. 

Command: `python setup.py bdist_msi`
"""

import distutils
import sys

from cx_Freeze import setup, Executable


# General App Info
version = "1.2.3"
application_id = "{7B9341F5-0D66-4442-4C5A-6430D22E9AA4}"  # Used for app upgrades
app_name = "Bom"
description = "Generate bill of materials of an articles #Fortune Br."
company = "Fortune Br"  # Made for

# Developer info: Try not to use these if you're copying codes written here ;-)
author = "kalaLokia"
author_email = "no-emails@kalalokia.xyz"
url = "https://github.com/kalaLokia/fbr_bom_app/releases"


# GUI app for windows, no console
base = "Win32GUI" if sys.platform == "win32" else None
icon = "icons/logo.ico"

# Exe file options
build_exe_options = {
    "packages": ["pyodbc", "sqlalchemy"],
    "include_files": [
        ("icons", "icons"),
        ("config.ini", "config.ini"),
        ("LICENSE", "license"),
    ],
    "excludes": ["tkinter"],
}

# Application shortcuts: Desktop, Start menu
shortcut_table = [
    (
        "DesktopShortcut",  # Shortcut
        "DesktopFolder",  # Directory_
        app_name,  # Name
        "TARGETDIR",  # Component_
        f"[TARGETDIR]{app_name}.exe",  # Target
        None,  # Arguments
        None,  # Description
        None,  # Hotkey
        None,  # Icon
        None,  # IconIndex
        None,  # ShowCmd
        "TARGETDIR",  # WkDir
    ),
    (
        "StartMenuShortcut",  # Shortcut
        "StartMenuFolder",  # Directory_
        app_name,  # Name
        "TARGETDIR",  # Component_
        f"[TARGETDIR]{app_name}.exe",  # Target
        None,  # Arguments
        None,  # Description
        None,  # Hotkey
        None,  # Icon
        None,  # IconIndex
        None,  # ShowCmd
        "TARGETDIR",  # WkDir
    ),
]

# Msi file options
ProgramFilesDir = (
    "ProgramFiles64Folder"
    if distutils.util.get_platform() == "win-amd64"
    else "ProgramFilesFolder"
)

bdist_msi_options = {
    "add_to_path": False,
    "install_icon": icon,
    "data": {"Shortcut": shortcut_table},
    "summary_data": {
        "author": author,
        "comments": f"Designed and developed by {author}",
        "keywords": "Bill of materials, Excel report, Costing",
    },
    "upgrade_code": application_id,
    "initial_target_dir": "[%s]\%s\%s" % (ProgramFilesDir, company, app_name),
}

# Executable settings
executable = Executable(
    "main.py",
    target_name=f"{app_name}.exe",
    icon=icon,
    copyright=f"Copyright (C) 2022 {author}",
    base=base,
)

setup(
    name=app_name,
    version=version,
    author=author,
    author_email=author_email,
    url=url,
    description=description,
    options={"build_exe": build_exe_options, "bdist_msi": bdist_msi_options},
    executables=[executable],
)
