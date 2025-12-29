from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import edge_tts
import uuid
import os

app = FastAPI(title="Edge TTS API")

# ---------- Request Model ----------
class TTSRequest(BaseModel):
    text: str
    voice: str = "en-GB-RyanNeural"
    is_ssml: bool = False

# ---------- Health Check ----------
@app.get("/")
def health():
    return {"status": "ok", "service": "edge-tts"}

# ---------- TTS Endpoint ----------
@app.post("/tts")
async def tts(req: TTSRequest):
    try:
        filename = f"/tmp/{uuid.uuid4()}.mp3"

        # ✅ CORRECT USAGE
        if req.is_ssml:
            communicate = edge_tts.Communicate(
                ssml=req.text,
                voice=req.voice
            )
        else:
            communicate = edge_tts.Communicate(
                text=req.text,
                voice=req.voice
            )

        await communicate.save(filename)

        return FileResponse(
            filename,
            media_type="audio/mpeg",
            filename="speech.mp3"
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
