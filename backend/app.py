from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
import asyncio
from camera_controller import CameraController
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

camera = CameraController()

class ConfigUpdate(BaseModel):
    iso: str | None = None
    aperture: str | None = None
    shutterspeed: str | None = None
    whitebalance: str | None = None

@app.on_event("startup")
def startup_event():
    try:
        camera.connect()
    except Exception as e:
        print(f"Startup camera connection failed: {e}")

@app.on_event("shutdown")
def shutdown_event():
    camera.disconnect()

@app.get("/api/status")
def get_status():
    return camera.get_status()

@app.post("/api/connect")
def connect_camera():
    try:
        camera.connect()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/config")
def get_config():
    try:
        return camera.get_all_configs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/config")
def set_config(config: ConfigUpdate):
    try:
        updates = {k: v for k, v in config.dict().items() if v is not None}
        if not updates:
            return {"status": "no updates provided"}
        results = camera.set_config(updates)
        return {"status": "success", "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/capture")
def capture_image():
    try:
        file_path = camera.capture_image()
        return {"status": "success", "file": os.path.basename(file_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/images/{filename}")
def get_image(filename: str):
    file_path = os.path.join("./captures", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Image not found")

async def gen_frames():
    while True:
        try:
            frame = await asyncio.to_thread(camera.capture_preview)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            await asyncio.sleep(0.05) # ~20 FPS limit
        except Exception as e:
            print(f"Preview error: {e}")
            await asyncio.sleep(1)

@app.get("/api/liveview")
def video_feed():
    if not camera.get_status()["connected"]:
        raise HTTPException(status_code=500, detail="Camera not connected")
    return StreamingResponse(gen_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

# Mount frontend static files last so API routes take precedence
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    os.makedirs("./captures", exist_ok=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)
