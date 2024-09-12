from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from .lighthouse_api import fetch_lighthouse_data
from .report_generator import create_report
from config import API_KEY

app = FastAPI()

class UrlInput(BaseModel):
    url: str
    strategy: str = "mobile"

@app.post("/generate_report/")
async def generate_report_endpoint(url_input: UrlInput, background_tasks: BackgroundTasks):
    try:
        data = fetch_lighthouse_data(url_input.url, API_KEY, url_input.strategy)
        output_file = f"report_{url_input.url.replace('https://', '').replace('http://', '').replace('/', '_')}.pdf"
        
        background_tasks.add_task(create_report, data, output_file, url_input.url)
        
        return {"message": "Report generation started", "file_name": output_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download_report/{file_name}")
async def download_report(file_name: str):
    file_path = f"./output/{file_name}"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="application/pdf", filename=file_name)
    raise HTTPException(status_code=404, detail="Report not found")
