# tasks.py
import os
import requests
from celery import Celery

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
GOTENBERG_URL = os.getenv('GOTENBERG_URL', 'http://localhost:3000')

celery_app = Celery('pdf_tasks', broker=CELERY_BROKER_URL, backend=CELERY_BROKER_URL)

@celery_app.task
def generate_pdf_from_html(html_content, output_path):
    files = {
        'index.html': ('index.html', html_content, 'text/html'),
    }
    response = requests.post(
        f"{GOTENBERG_URL}/forms/chromium/convert/html",
        files=files,
    )
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return output_path
    else:
        raise Exception(f"Gotenberg error: {response.status_code} {response.text}")
