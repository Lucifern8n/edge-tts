from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
import edge_tts
import uuid

app = FastAPI(title="Edge TTS API")

@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/tts")
async def tts(
    text: str = Query(...),
    voice: str = Query("en-US-JennyNeural"),
    style: str | None = Query(None),
    rate: str = Query("+0%"),
    pitch: str = Query("+0Hz"),
    format: str = Query("mp3")
):
    try:
        filename = f"/tmp/{uuid.uuid4()}.{format}"

        # 🔑 AUTO-DETECT SSML
        is_ssml = text.strip().startswith("<speak>")

        if is_ssml:
            # Use SSML exactly as provided
            payload = text

        elif style:
            # Build SSML only when style is requested
            payload = f"""
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
        else:
            # Plain text (safe for DavisNeural)
            payload = text

        communicate = edge_tts.Communicate(
            text=payload,
            voice=voice
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
