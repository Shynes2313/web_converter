from fastapi import FastAPI, Request, Response, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import shutil
import os

app = FastAPI(title="Web Media Converter")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # നിങ്ങളുടെ മറ്റ് അപ്‌ലോഡ് കോഡുകൾ ഇവിടെ നൽകുക
    pass
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
