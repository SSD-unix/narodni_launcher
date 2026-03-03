NARODNI LAUNCHER (Python Version)

NARODNI LAUNCHER is an open-source Minecraft launcher for version a1.1.2_01.
It is designed for Linux users and runs directly through Python, without requiring pre-built binaries.
It includes all necessary files to start playing and managing servers like Planet Nostalgia.

This guide is for complete beginners, explaining how to install Python, required libraries, and run the launcher.

🌟 Features

Runs directly with Python 3 (no binary packaging required)

Full Linux support (Ubuntu, Debian, Fedora)

Integrated support for Minecraft servers

Provides housing and resources for new players

Uses PyQt6 for GUI and QWebEngineView for server news and updates

Lightweight and optimized for old Minecraft versions

Open-source and completely free

Easy to extend or customize for your own servers

Works with LWJGL libraries included in libs/nativate/

Supports textures, icons, and custom launcher images

Tracks player nickname and settings in startdef.txt

Beginner-friendly with step-by-step instructions

Debug mode for developers

Automatic handling of Java library paths

Supports multiple Minecraft accounts

Allows adding or removing servers easily

🐍 Step 1: Install Python

NARODNI LAUNCHER requires Python 3.10+.

Ubuntu / Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv
Fedora
sudo dnf install python3 python3-pip python3-venv

Verify Python installation:

python3 --version

You should see something like:

Python 3.10.12
📦 Step 2: Install Required Python Libraries

The launcher uses these modules:

Standard Python: sys, os, subprocess

PyQt6 GUI: PyQt6, PyQt6.QtWidgets, PyQt6.QtCore, PyQt6.QtGui

PyQt6 WebEngine: PyQt6.QtWebEngineWidgets

Install libraries via pip:

python3 -m pip install --upgrade pip
python3 -m pip install PyQt6 PyQt6-WebEngine
📁 Step 3: Download NARODNI LAUNCHER Source

Download via GitHub or ZIP.
Ensure the following structure is present:

NARODNI-Launcher/
├── launch.py          # main Python script
├── a1.1.2_01.jar      # Minecraft client
├── libs/              # required JAR files
│   └── nativate/      # .so files for LWJGL/OpenAL
├── res/               # images and textures
├── startdef.txt       # configuration file
└── README.md          # this guide
🚀 Step 4: Run the Launcher

Run the launcher directly from Python:

python3 launch.py

The launcher GUI will open

It will automatically load the Minecraft client, textures, and libraries

New players will be given housing and resources

You can select servers, log in with your nickname, and start playing

⚙️ Step 5: Configure Minecraft Natives (LWJGL)

If you encounter errors like:

NoClassDefFoundError: org/lwjgl/LWJGLException

Ensure:

libs/nativate/ contains correct .so files for your system

launch.py uses the correct Java library path:

import subprocess, os

DIR = os.path.dirname(os.path.abspath(__file__))
java_cmd = [
    "java",
    f"-Djava.library.path={os.path.join(DIR, 'libs', 'nativate')}",
    "-cp",
    ":".join([
        os.path.join(DIR, "a1.1.2_01.jar"),
        os.path.join(DIR, "libs/lwjgl.jar"),
        os.path.join(DIR, "libs/lwjgl_util.jar"),
        os.path.join(DIR, "libs/jinput.jar")
    ]),
    "net.minecraft.client.Minecraft",
    "--username", "your_nickname"
]
subprocess.run(java_cmd)

Tip: Use absolute paths if necessary.

🔹 Step 6: File Structure Overview
NARODNI-Launcher/
├── launch.py            # main Python script
├── a1.1.2_01.jar        # Minecraft client
├── libs/                # JARs and native libraries
│   └── nativate/        # .so files for LWJGL/OpenAL
├── res/                 # images and textures
├── startdef.txt         # launcher configuration
└── README.md            # this guide
🛠️ Step 7: Make Python Executable (Optional)
chmod +x launch.py
./launch.py

Run launcher without typing python3.

If you want, I can also make a more GitHub-friendly version with badges, table of contents, and emojis to make it look really professional. It will look like a top-tier open-source launcher README.

Do you want me to do that?
