# tasks.py
import os
import requests
from celery import Celery
from datetime import datetime

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
GOTENBERG_URL = os.getenv('GOTENBERG_URL', 'http://localhost:3000')

celery_app = Celery('pdf_tasks', broker=CELERY_BROKER_URL, backend=CELERY_BROKER_URL)

@celery_app.task(bind=True)
def generate_multiple_pdfs(self, html_template, output_dir, count):
    """
    Generate multiple PDFs and report progress.
    :param html_template: HTML template string with {i} for numbering.
    :param output_dir: Directory to save PDFs.
    :param count: How many PDFs to generate.
    """
    date_str = datetime.now().strftime('%Y-%m-%d')
    results = []
    for i in range(1, count + 1):
        html_content = html_template.format(i=i)
        output_path = os.path.join(output_dir, f"hello-{date_str}-{i:04d}.pdf")
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
            results.append(output_path)
        else:
            # Optionally, you can stop or skip on error
            raise Exception(f"Gotenberg error: {response.status_code} {response.text}")
        # Update progress after each PDF
        self.update_state(
            state='PROGRESS',
            meta={
                'current': i,
                'total': count,
                'last_file': output_path
            }
        )
    return results