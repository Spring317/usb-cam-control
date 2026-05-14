import os
import sys

# If running from PyInstaller bundle, set up environment for libgphoto2
if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
    os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = bundle_dir + os.pathsep + os.environ.get("DYLD_FALLBACK_LIBRARY_PATH", "")
    
    # Locate the plugin directories included by PyInstaller
    for d in os.listdir(os.path.join(bundle_dir, "libgphoto2_port")):
        os.environ["IOLIBS"] = os.path.join(bundle_dir, "libgphoto2_port", d)
    for d in os.listdir(os.path.join(bundle_dir, "libgphoto2")):
        os.environ["CAMLIBS"] = os.path.join(bundle_dir, "libgphoto2", d)

import uvicorn
import threading
import webview
import time
from backend.app import app

def start_server():
    # Run the uvicorn server in a separate thread
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")

if __name__ == '__main__':
    # Start the backend server
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Wait a moment for the server to start
    time.sleep(1)
    
    # Create the native desktop window
    webview.create_window('Canon EOS R8 Control', 'http://127.0.0.1:8000', width=1200, height=800)
    webview.start()
