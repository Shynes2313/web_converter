from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
import shutil
import os

app = FastAPI(title="Web Media Converter")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
   @app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    return {"info": f"file '{file.filename}' saved successfully"}
