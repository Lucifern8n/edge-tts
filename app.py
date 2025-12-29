from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel  # <--- THIS WAS MISSING OR PLACED WRONG
import edge_tts
import uuid

app = FastAPI(title="Edge TTS API")

# Define the request structure
class TTSRequest(BaseModel):
    text: str
    voice: str = "en-GB-RyanNeural"
    rate: str = "-15%" 
    pitch: str = "-5%"

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/tts")
async def tts(req: TTSRequest):
    try:
        filename = f"/tmp/{uuid.uuid4()}.mp3"

        # Pass rate and pitch directly to Communicate
        communicate = edge_tts.Communicate(
            text=req.text,
            voice=req.voice,
            rate=req.rate,
            pitch=req.pitch
        )

        await communicate.save(filename)

        return FileResponse(filename, media_type="audio/mpeg")

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
