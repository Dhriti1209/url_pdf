from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_BROKER_URL = os.getenv("REDIS_BROKER_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "worker",
    broker=REDIS_BROKER_URL,
    backend=REDIS_BROKER_URL
)

celery_app.conf.task_routes = {
    'tasks.generate_pdf_task': {'queue': 'pdf'}
}
