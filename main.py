from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from celery.result import AsyncResult
from tasks import generate_pdf_task
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
STORAGE_PATH = os.getenv("PDF_STORAGE_PATH", "./storage")


class URLInput(BaseModel):
    url: str


@app.post("/generate")
async def generate_pdf(data: URLInput):
    task = generate_pdf_task.delay(data.url)
    return {"task_id": task.id}


@app.get("/status/{task_id}")
def get_status(task_id: str):
    result = AsyncResult(task_id)
    return {"status": result.status, "result": result.result}


@app.get("/download/{filename}")
def download_file(filename: str):
    file_path = os.path.join(STORAGE_PATH, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return JSONResponse(status_code=404, content={"message": "File not found"})
