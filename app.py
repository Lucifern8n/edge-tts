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

        # ✅ USE SSML ONLY WHEN STYLE IS PROVIDED
        if style:
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
            # ✅ DAVISNEURAL WORKS BEST WITH PLAIN TEXT
            payload = text

        communicate = edge_tts.Communicate(
            text=payload,
            voice=voice
        )

        await communicate.save(filename)

        return FileRespon
