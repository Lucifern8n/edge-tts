from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import edge_tts
import uuid

app = FastAPI(title="Edge TTS API")

# ---------- Request Model ----------
class TTSRequest(BaseModel):
    text: str
    voice: str = "en-GB-RyanNeural"
    rate: str | None = None     # e.g. "-10%"
    pitch: str | None = None    # e.g. "-3Hz"
    style: str | None = None    # e.g. "chat"
    is_ssml: bool = False       # set true if text already contains <speak>

# ---------- Health ----------
@app.get("/")
def health():
    return {"status": "ok"}

# ---------- TTS ----------
@app.post("/tts")
async def tts(req: TTSRequest):
    try:
        filename = f"/tmp/{uuid.uuid4()}.mp3"

        # ---------- Build SSML if needed ----------
        if req.is_ssml:
            ssml = req.text

        elif req.rate or req.pitch or req.style:
            prosody_attrs = []
            if req.rate:
                prosody_attrs.append(f'rate="{req.rate}"')
            if req.pitch:
                prosody_attrs.append(f'pitch="{req.pitch}"')

            prosody_attr_str = " ".join(prosody_attrs)

            if req.style:
                ssml = f"""
<speak>
  <voice name="{req.voice}">
    <express-as style="{req.style}">
      <prosody {prosody_attr_str}>
        {req.text}
      </prosody>
    </express-as>
  </voice>
</speak>
"""
            else:
                ssml = f"""
<speak>
  <voice name="{req.voice}">
    <prosody {prosody_attr_str}>
      {req.text}
    </prosody>
  </voice>
</speak>
"""

        else:
            ssml = None

        # ---------- Call Edge-TTS ----------
        if ssml:
            communicate = edge_tts.Communicate(
                ssml=ssml,
                voice=req.voice
            )
        else:
            communicate = edge_tts.Communicate(
                text=req.text,
                voice=req.voice
            )

        await communicate.save(filename)

        return FileResponse(filename, media_type="audio/mpeg")

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
