# submit_task.py
import os
from datetime import datetime
from glob import glob
from tasks import generate_pdf_from_html

# 1. Get current date string
date_str = datetime.now().strftime('%Y-%m-%d')

html_content = "<h1>Hello World!</h1>"
output_path = f"/tmp/hello-{date_str}.pdf"
result = generate_pdf_from_html.delay(html_content, output_path)
print(f"Task submitted! Task ID: {result.id}")
print(f"You can check the result with:")
print(f"    python3 check_result.py {result.id}")
