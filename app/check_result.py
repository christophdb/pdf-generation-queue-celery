import sys
from tasks import celery_app

if len(sys.argv) != 2:
    print("Error: No task_id provided.\nUsage: python3 check_result.py <task_id>")
    sys.exit(1)

task_id = sys.argv[1]
result = celery_app.AsyncResult(task_id)

if result.state == 'PROGRESS':
    meta = result.info
    print(f"Progress: {meta['current']} of {meta['total']} PDFs generated. Last: {meta['last_file']}")
elif result.ready():
    print("Task finished!")
    print("Generated files:")
    for fname in result.get():
        print(f"  {fname}")
else:
    print("Task still running or pending.")