# NARODNI LAUNCHER (Python Version)

**NARODNI LAUNCHER** is an **open-source Minecraft launcher** for version `a1.1.2_01`.  
This launcher is specially designed for **Linux users** and runs directly through Python, without requiring any pre-built binaries.  
It includes everything you need to start playing and managing servers like Planet Nostalgia.

---

## 🌟 Features

- Runs directly with Python 3 (no binary packaging needed)
- Full Linux support (Ubuntu, Debian, Fedora)
- Integrated support for Minecraft servers
- Provides housing and resources for new players
- Uses **PyQt6** for GUI and **QWebEngineView** for server news and updates
- Lightweight and optimized for old Minecraft versions
- Open-source and completely free
- Easy to extend or customize for your own servers
- Works with LWJGL libraries included in `libs/nativate/`
- Supports textures, icons, and custom launcher images
- Tracks player nickname and settings in `startdef.txt`
- Beginner-friendly with step-by-step instructions

---

## 🐍 Step 1: Install Python

NARODNI LAUNCHER requires **Python 3.10+** to work properly.  
Python 3 is already installed on most modern Linux distributions, but if you don't have it, follow these instructions.

### Ubuntu / Debian:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
Fedora:
sudo dnf install python3 python3-pip python3-venv
Check Python version:
python3 --version

You should see something like:

Python 3.10.12
📦 Step 2: Install Required Python Libraries

NARODNI LAUNCHER depends on several Python modules:

Standard Python modules: sys, os, subprocess

PyQt6 GUI modules: PyQt6, PyQt6.QtWidgets, PyQt6.QtCore, PyQt6.QtGui

PyQt6 WebEngine module: PyQt6.QtWebEngineWidgets (for QWebEngineView)

Install them using pip:

python3 -m pip install --upgrade pip
python3 -m pip install PyQt6 PyQt6-WebEngine

This ensures all GUI components, windows, buttons, and the embedded web view work correctly.

📁 Step 3: Download NARODNI LAUNCHER Source

You can download the launcher source files as a ZIP or clone from GitHub:

git clone https://github.com/USERNAME/NARODNI-Launcher.git
cd NARODNI-Launcher

Make sure the following files are present:

launch.py          # main Python script
a1.1.2_01.jar      # Minecraft client
libs/              # all required JAR files
    └── nativate/  # .so files for LWJGL/OpenAL
res/               # images and textures for launcher
startdef.txt       # configuration and default settings
README.md          # this guide
🚀 Step 4: Run the Launcher

Run the launcher directly from Python:

python3 launch.py

The launcher GUI will open immediately

It will automatically load Minecraft client, textures, and libraries

You can select servers, login with your nickname, and start playing

New players will be given housing and basic resources automatically

⚙️ Step 5: Configure Minecraft Natives (LWJGL)

If you see errors like:

NoClassDefFoundError: org/lwjgl/LWJGLException

Follow these steps:

Ensure the folder libs/nativate/ contains the correct .so files for your system:

liblwjgl64.so for 64-bit Java

libopenal64.so for 64-bit Java

Make sure your launch.py uses the correct Java library path:

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

Use absolute paths if you encounter further errors.

🔹 Step 6: File Structure
NARODNI-Launcher/
├── launch.py            # main Python script
├── a1.1.2_01.jar        # Minecraft client
├── libs/                # all required JAR files
│   └── nativate/        # .so files for LWJGL/OpenAL
├── res/                 # launcher images and textures
├── startdef.txt         # launcher configuration
└── README.md            # this guide

Keep this structure intact; the launcher will not work if libs/ or res/ are moved.

🛠️ Step 7: Make Python Executable (Optional)

You can make launch.py executable for easier launching:

chmod +x launch.py
./launch.py

This allows running the launcher without typing python3 every time.

📢 Step 8: Troubleshooting
LWJGL / OpenAL Errors

Ensure .so files in libs/nativate/ match your Java architecture

Use 64-bit Java with 64-bit .so files

Verify -Djava.library.path points to the correct folder

PyQt6 Issues

Make sure PyQt6 and PyQt6-WebEngine are installed:

python3 -m pip install PyQt6 PyQt6-WebEngine
Java Not Found

Install OpenJDK 17 or newer:

sudo apt install openjdk-17-jre
🔹 Step 9: Adding Servers

Servers are configured inside startdef.txt

You can add/remove servers manually

Supported servers: Planet Nostalgia, custom Alpha servers

Launcher handles housing, resources, and player management automatically

📢 Step 10: Contributing

This project is open-source under MIT License

Pull requests, bug reports, and feature suggestions are welcome

Contact developer: Davit Sargsyan

⚖️ License

MIT License — free to use, modify, and distribute.

📝 Tips for Beginners

Always launch from the folder containing launch.py

Make sure Java is installed and java -version shows 64-bit

Ensure libs/nativate/ and a1.1.2_01.jar are present

Install Python 3.10+ and required PyQt6 modules

For advanced debugging, run python3 launch.py from terminal to see logs
