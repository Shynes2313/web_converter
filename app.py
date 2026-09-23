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
