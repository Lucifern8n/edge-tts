class TTSRequest(BaseModel):
    text: str
    voice: str = "en-GB-RyanNeural"
    rate: str = "-15%"  # Default slower speed
    pitch: str = "-5%"  # Default deeper voice

@app.post("/tts")
async def tts(req: TTSRequest):
    try:
        filename = f"/tmp/{uuid.uuid4()}.mp3"

        # Using the variables from the request
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
