import gphoto2 as gp
import logging

logging.basicConfig(level=logging.INFO)

context = gp.Context()
camera = gp.Camera()
camera.init(context)

print("Connected. Testing preview...")
try:
    preview = camera.capture_preview(context)
    print("Preview captured:", preview.get_data_and_size()[1], "bytes")
except Exception as e:
    print("Preview failed:", e)

print("Testing capture...")
try:
    file_path = camera.capture(gp.GP_CAPTURE_IMAGE, context)
    print("Captured:", file_path.name)
except Exception as e:
    print("Capture failed:", e)

camera.exit(context)
