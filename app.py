from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import edge_tts
import uuid

app = FastAPI(title="Edge TTS API")

class TTSRequest(BaseModel):
    text: str
    voice: str = "en-GB-RyanNeural"
    rate: str = "-15%"
    pitch: str = "-10Hz"  # Use Hz for a safer, more reliable "deep" voice

@app.post("/tts")
async def tts(req: TTSRequest):
    try:
        filename = f"/tmp/{uuid.uuid4()}.mp3"

        communicate = edge_tts.Communicate(
            text=req.text,
            voice=req.voice,
            rate=req.rate,
            pitch=req.pitch
        )

        await communicate.save(filename)
        return FileResponse(filename, media_type="audio/mpeg")

    except Exception as e:
        # This will help us see exactly what the library didn't like
        return JSONResponse(status_code=400, content={"error": str(e)})
        
@app.get("/ping")
async def ping():
    return {"status": "ok"}
