# check_result.py
import sys
from tasks import celery_app

if len(sys.argv) != 2:
    print("Usage: python3 check_result.py <task_id>")
    sys.exit(1)

task_id = sys.argv[1]
result = celery_app.AsyncResult(task_id)
if result.ready():
    print(f"PDF saved at: {result.get()}")
else:
    print("Task still running or failed.")
