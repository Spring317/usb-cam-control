# Canon EOS R8 Control App

## Introduction
A cross-platform local web application to fully control a Canon EOS R8 (and other compatible Canon EOS cameras) over USB. This project bypasses the need for Canon's CCAPI by utilizing `gphoto2` to interface directly with the camera hardware via PTP (Picture Transfer Protocol). It provides a beautiful, modern web interface to view the live sensor feed, adjust settings, and capture high-resolution images directly to your computer.

## Features
- **Live View Stream:** High-speed MJPEG stream of the camera's sensor directly in your web browser.
- **Remote Configuration:** Adjust ISO, Aperture, Shutter Speed, and White Balance on the fly.
- **Direct PC Capture:** Take photos over USB and automatically download them to the local `captures/` directory with continuous 7-digit filename sequencing to prevent overwriting.
- **Virtual Webcam Routing (Linux):** Included script to pipe the camera's live view into a virtual webcam (`/dev/video0`) for use in OBS, Zoom, or Discord without needing official Canon webcam software.
- **Modern Premium UI:** A responsive, dark-mode, frosted-glass interface built with pure HTML/CSS/JS.

## Prerequisites
Before you begin, ensure you have the following installed on your system:

### Linux (Ubuntu/Debian-based)
You must install the system-level `libgphoto2` dependencies for the Python bindings to work:
```bash
sudo apt update
sudo apt install libgphoto2-dev libexif-dev libltdl-dev libusb-dev python3-venv
```

If you wish to use the virtual webcam routing functionality, install ffmpeg and v4l2loopback:
```bash
sudo apt install ffmpeg v4l2loopback-dkms
```

### Windows
Running this natively on Windows requires specific libusb driver replacements via Zadig or MSYS2 compilation. It is highly recommended to run this inside **WSL2** (Windows Subsystem for Linux) and pass your USB device through to WSL using `usbipd-win`.

### macOS
A fully standalone native macOS `.app` bundle and `.dmg` installer is automatically built via GitHub Actions. You do **not** need to manually install dependencies or run the python backend if you simply want to use the application! See the Usage section below.

## Installation Setup

1. **Clone the repository and enter the directory:**
```bash
cd cam-control
```

2. **Create and activate a Python virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. **Install the required Python dependencies:**
```bash
pip install -r requirements.txt
```

## Usage

### 1. Web Dashboard
1. Connect your Canon EOS R8 to your computer via USB.
2. Turn the camera on. For the best remote control experience, switch the camera dial to **Manual (M)** mode.
3. Ensure no other applications (like `gvfs` file managers or EOS Utility) are currently accessing the camera.
4. Start the FastAPI backend server:
```bash
python backend/app.py
```
5. Open your web browser and navigate to `http://localhost:8000`.
6. Click **Connect** to start the live view and begin controlling the camera! Captured images will be saved automatically to the `captures/` folder.

### 2. Virtual Webcam (Linux only)
If you only want to use the camera as a webcam in video conferencing apps:
```bash
./scripts/start_webcam.sh
```
This script configures `v4l2loopback` and pipes the `gphoto2` live feed directly into a virtual video device.

### 3. macOS Native Application
For macOS users, a beautifully packaged native desktop application is automatically compiled for you:
1. Navigate to the **Actions** tab of your GitHub repository.
2. Click on the latest successful run of the **Build macOS App** workflow.
3. Scroll down to the **Artifacts** section and download the `CanonControl-macOS.dmg` file.
4. Double-click the `.dmg` file and drag the `CanonControl` app to your Applications folder.
5. Connect your camera, open the app, and you're ready to go!
*Note: Because this app is built via GitHub Actions and is unsigned, you may need to **Right-Click -> Open** the app the very first time to bypass Apple's Gatekeeper security warning.*
