import os
import shutil
import subprocess
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request, Response
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Web Media Converter")
templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), convert_to: str = "mp3"):
    try:
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file_base_name, _ = os.path.splitext(file.filename)
        output_filename = f"{file_base_name}.{convert_to}"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        
        cmd = ["ffmpeg", "-y", "-i", input_path, output_path]
        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if process.returncode != 0:
            raise HTTPException(status_code=500, detail="Conversion failed using FFmpeg")
        
        return FileResponse(output_path, media_type="application/octet-stream", filename=output_filename)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
import shutil
import os
import subprocess
from fastapi import FastAPI, Request, Response, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Web Media Converter")
templates = Jinja2Templates(directory="templates")
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...), 
    convert_to: str = Form("mp3"), 
    start_time: str = Form("0"), 
    end_time: str = Form("10")
):
    try:
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file_base_name, _ = os.path.splitext(file.filename)
        output_filename = f"{file_base_name}.{convert_to}"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        cmd = ["ffmpeg", "-y", "-ss", start_time, "-to", end_time, "-i", input_path, output_path]
        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if process.returncode != 0:
            raise HTTPException(status_code=500, detail="Conversion failed using FFmpeg")
        
        return FileResponse(output_path, media_type="application/octet-stream", filename=output_filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
