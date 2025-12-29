from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import edge_tts
import uuid

app = FastAPI(title="Edge TTS API")

class TTSRequest(BaseModel):
    text: str
    voice: str = "en-GB-RyanNeural"
    rate: str | None = None
    pitch: str | None = None
    style: str | None = None
    is_ssml: bool = False

@app.post("/tts")
async def tts(req: TTSRequest):
    try:
        filename = f"/tmp/{uuid.uuid4()}.mp3"

        # ---------- Build SSML if needed ----------
        if req.is_ssml or req.rate or req.pitch or req.style:
            prosody = []
            if req.rate:
                prosody.append(f'rate="{req.rate}"')
            if req.pitch:
                prosody.append(f'pitch="{req.pitch}"')

            prosody_str = " ".join(prosody)

            if req.style:
                ssml = f"""
<speak>
  <voice name="{req.voice}">
    <express-as style="{req.style}">
      <prosody {prosody_str}>
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
    <prosody {prosody_str}>
      {req.text}
    </prosody>
  </voice>
</speak>
"""
            text_input = ssml
            is_ssml = True
        else:
            text_input = req.text
            is_ssml = False

        communicate = edge_tts.Communicate(
            text=text_input,
            voice=req.voice,
            is_ssml=is_ssml   # ✅ THIS IS THE CORRECT FLAG
        )

        await communicate.save(filename)

        return FileResponse(filename, media_type="audio/mpeg")

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
