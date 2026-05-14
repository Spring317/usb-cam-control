import gphoto2 as gp
import threading
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CameraController:
    def __init__(self):
        self.camera = None
        self.context = gp.Context()
        self.lock = threading.Lock()
        self._connected = False

    def connect(self):
        with self.lock:
            if not self._connected:
                try:
                    self.camera = gp.Camera()
                    self.camera.init(self.context)
                    self._connected = True
                    logger.info("Camera connected successfully.")

                    # Configure Canon specific settings for live view and capture
                    try:
                        config = self.camera.get_config(self.context)
                        
                        # Enable viewfinder for capture_preview
                        try:
                            vf = config.get_child_by_name('viewfinder')
                            vf.set_value(1)
                        except:
                            pass
                            
                        # Set capture target to SDRAM to avoid SD card lock errors
                        try:
                            ct = config.get_child_by_name('capturetarget')
                            ct.set_value(1)
                        except:
                            pass

                        self.camera.set_config(config, self.context)
                        logger.info("Configured viewfinder and capturetarget.")
                    except Exception as e:
                        logger.warning(f"Could not apply initial configs: {e}")

                except gp.GPhoto2Error as e:
                    logger.error(f"Failed to connect to camera: {e}")
                    self.camera = None
                    self._connected = False
                    raise Exception(f"Failed to connect to camera: {e}")
            return self._connected

    def disconnect(self):
        with self.lock:
            if self._connected and self.camera:
                self.camera.exit(self.context)
            self._connected = False
            self.camera = None

    def get_status(self):
        return {"connected": self._connected}

    def _get_config_value(self, name):
        try:
            config = self.camera.get_config(self.context)
            widget = config.get_child_by_name(name)
            value = widget.get_value()
            choices = []
            if widget.get_type() == gp.GP_WIDGET_RADIO or widget.get_type() == gp.GP_WIDGET_MENU:
                for i in range(widget.count_choices()):
                    choices.append(widget.get_choice(i))
            return {"value": value, "choices": choices}
        except gp.GPhoto2Error:
            return None

    def _set_config_value(self, name, value):
        try:
            config = self.camera.get_config(self.context)
            widget = config.get_child_by_name(name)
            widget.set_value(value)
            self.camera.set_config(config, self.context)
            return True
        except gp.GPhoto2Error as e:
            logger.error(f"Error setting {name} to {value}: {e}")
            return False

    def get_all_configs(self):
        with self.lock:
            if not self._connected:
                raise Exception("Camera not connected")
            # Usually we care about iso, aperture, shutterspeed, whitebalance
            stats = {
                "iso": self._get_config_value("iso"),
                "aperture": self._get_config_value("aperture"),
                "shutterspeed": self._get_config_value("shutterspeed"),
                "whitebalance": self._get_config_value("whitebalance")
            }
            return stats

    def set_config(self, config_dict):
        with self.lock:
            if not self._connected:
                raise Exception("Camera not connected")
            results = {}
            for key, val in config_dict.items():
                results[key] = self._set_config_value(key, val)
            return results

    def capture_image(self, download_dir=None):
        with self.lock:
            if not self._connected:
                raise Exception("Camera not connected")
            
            if download_dir is None:
                download_dir = os.path.expanduser("~/Pictures/CanonCaptures")

            if not os.path.exists(download_dir):
                os.makedirs(download_dir)

            try:
                import time
                config = self.camera.get_config(self.context)
                
                # Temporarily disable viewfinder to allow capture
                vf = None
                try:
                    vf = config.get_child_by_name('viewfinder')
                    vf.set_value(0)
                    self.camera.set_config(config, self.context)
                    logger.info("Disabled viewfinder for capture")
                    time.sleep(0.5) # Wait for mirror/shutter to settle
                except Exception as e:
                    logger.debug(f"Could not disable viewfinder: {e}")
                
                # Capture
                file_path = self.camera.capture(gp.GP_CAPTURE_IMAGE, self.context)
                
                # Determine new 7-digit continuous filename
                import glob
                import re
                existing_files = glob.glob(os.path.join(download_dir, "*.*"))
                max_num = 0
                for f in existing_files:
                    basename = os.path.basename(f)
                    match = re.match(r'^(\d{7})\.', basename)
                    if match:
                        num = int(match.group(1))
                        if num > max_num:
                            max_num = num
                
                new_num = max_num + 1
                ext = os.path.splitext(file_path.name)[1]
                if not ext:
                    ext = ".jpg" # fallback
                new_filename = f"{new_num:07d}{ext}"
                
                # Download
                target_path = os.path.join(download_dir, new_filename)
                camera_file = gp.CameraFile()
                self.camera.file_get(file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL, camera_file, self.context)
                camera_file.save(target_path)
                
                # Re-enable viewfinder
                if vf:
                    try:
                        vf.set_value(1)
                        self.camera.set_config(config, self.context)
                        logger.info("Re-enabled viewfinder after capture")
                    except Exception as e:
                        logger.debug(f"Could not re-enable viewfinder: {e}")
                
                return target_path
            except gp.GPhoto2Error as e:
                import traceback
                logger.error(f"Failed to capture image: {e}\n{traceback.format_exc()}")
                raise Exception(f"Failed to capture image: {e}")

    def capture_preview(self):
        with self.lock:
            if not self._connected:
                raise Exception("Camera not connected")
            try:
                camera_file = gp.CameraFile()
                self.camera.capture_preview(camera_file, self.context)
                file_data = camera_file.get_data_and_size()
                return memoryview(file_data).tobytes()
            except gp.GPhoto2Error as e:
                logger.error(f"Failed to capture preview: {e}")
                raise Exception(f"Failed to capture preview: {e}")
