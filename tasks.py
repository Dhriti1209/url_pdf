from celery_worker import celery_app
import subprocess
import os
import uuid
from dotenv import load_dotenv

load_dotenv()
STORAGE_PATH = os.getenv("PDF_STORAGE_PATH", "./storage")


@celery_app.task(name="tasks.generate_pdf_task")
def generate_pdf_task(url: str):
    filename = f"{uuid.uuid4()}.pdf"
    filepath = os.path.join(STORAGE_PATH, filename)
    command = ["node", "utils/puppeteer_call.js", url, filepath]

    try:
        subprocess.run(command, check=True)
        return filename
    except Exception as e:
        return str(e)
