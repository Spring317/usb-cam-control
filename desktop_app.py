import os
import sys

# If running from PyInstaller bundle, set up environment for libgphoto2
if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
    os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = bundle_dir + os.pathsep + os.environ.get("DYLD_FALLBACK_LIBRARY_PATH", "")
    
    # Only needed when the Homebrew libgphoto2 was bundled (gphoto2 built from
    # source). The PyPI wheel ships its own camlibs/iolibs and points
    # CAMLIBS/IOLIBS at them itself on import.
    for env, sub in (("IOLIBS", "libgphoto2_port"), ("CAMLIBS", "libgphoto2")):
        plugin_root = os.path.join(bundle_dir, sub)
        if os.path.isdir(plugin_root):
            for d in os.listdir(plugin_root):
                os.environ[env] = os.path.join(plugin_root, d)
else:
    # backend/app.py imports camera_controller as a top-level module
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))

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
