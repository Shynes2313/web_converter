import os
import uuid
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from moviepy.editor import VideoFileClip, AudioFileClip

app = FastAPI(title="Web Media Converter")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/convert")
async def convert_file(
    file: UploadFile = File(...),
    target_format: str = Form(...)
):
    target_format = target_format.lower().strip()
    allowed_formats = ["mp3", "wav", "aac", "mp4", "mkv"]
    
    if target_format not in allowed_formats:
        raise HTTPException(status_code=400, detail="ഈ ഫോർമാറ്റ് സപ്പോർട്ട് ചെയ്യുന്നില്ല.")

    file_id = str(uuid.uuid4())
    input_ext = os.path.splitext(file.filename)[1]
    input_path = os.path.join(UPLOAD_DIR, f"{file_id}_input{input_ext}")
    output_filename = f"{file_id}_output.{target_format}"
    output_path = os.path.join(UPLOAD_DIR, output_filename)

    with open(input_path, "wb") as buffer:
        buffer.write(await file.read())

    try:
        audio_formats = ["mp3", "wav", "aac"]
        video_formats = ["mp4", "mkv"]

        if target_format in audio_formats:
            clip = VideoFileClip(input_path) if input_ext.lower() in [".mp4", ".mkv", ".avi", ".mov"] else AudioFileClip(input_path)
            clip.audio.write_audiofile(output_path) if hasattr(clip, 'audio') and clip.audio else clip.write_audiofile(output_path)
            clip.close()

        elif target_format in video_formats:
            clip = VideoFileClip(input_path)
            clip.write_videofile(output_path, codec="libx264")
            clip.close()

        if os.path.exists(input_path):
            os.remove(input_path)

        return FileResponse(
            path=output_path,
            filename=f"converted_{os.path.splitext(file.filename)[0]}.{target_format}",
            media_type="application/octet-stream"
        )

    except Exception as e:
        if os.path.exists(input_path):
            os.remove(input_path)
        raise HTTPException(status_code=500, detail=f"കൺവേർഷൻ തടസ്സപ്പെട്ടു: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)