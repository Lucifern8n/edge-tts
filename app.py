@app.post("/tts")
async def tts(req: TTSRequest):
    try:
        filename = f"/tmp/{uuid.uuid4()}.mp3"

        # Adjust these values to your liking:
        # rate="-20%" makes it slower
        # pitch="-10Hz" or "-5%" makes it deeper
        # volume="+0%" is default
        
        ssml_text = f"""
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
            <voice name='{req.voice}'>
                <prosody rate='-15%' pitch='-5%'>
                    {req.text}
                </prosody>
            </voice>
        </speak>
        """

        communicate = edge_tts.Communicate(
            text=ssml_text, 
            voice=req.voice
        )

        await communicate.save(filename)
        return FileResponse(filename, media_type="audio/mpeg")

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
