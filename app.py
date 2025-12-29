from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
import edge_tts
import uuid

app = FastAPI(title="Edge TTS API")

@app.get("/")
def health():
    return {"status": "ok", "message": "Edge TTS API running"}

@app.get("/tts")
async def tts(
    text: str = Query(...),
    voice: str = Query("en-US-JennyNeural"),
    style: str = Query("cheerful"),
    rate: str = Query("+0%"),
    pitch: str = Query("+0Hz"),
    format: str = Query("mp3")
):
    try:
        filename = f"/tmp/{uuid.uuid4()}.{format}"

        ssml = f"""
<speak>
  <voice name="{voice}">
    <express-as style="{style}">
      <prosody rate="{rate}" pitch="{pitch}">
        {text}
      </prosody>
    </express-as>
  </voice>
</speak>
"""

        communicate = edge_tts.Communicate(
            text=ssml,
            voice=voice
        )

        await communicate.save(filename)

        return FileResponse(
            filename,
            media_type="audio/mpeg",
            filename="speech.mp3"
        )

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
