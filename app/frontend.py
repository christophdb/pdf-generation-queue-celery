import os
from flask import Flask, render_template_string, request, redirect, url_for
from celery import Celery
from celery.result import AsyncResult
from tasks import generate_multiple_pdfs  # Import your Celery task

# Configure Celery (adjust as needed)
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
celery_app = Celery('pdf_tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

# Store submitted task IDs (in-memory for demo; use DB for production)
TASK_IDS = []

app = Flask(__name__)

@app.route('/start', methods=['POST'])
def start_task():
    count = int(request.form.get('count', 20))
    html_template = "<h1>Hello World! PDF #{i}</h1>"
    output_dir = "/tmp"
    result = generate_multiple_pdfs.delay(html_template, output_dir, count)
    TASK_IDS.append(result.id)
    return redirect(url_for('index', new_task_id=result.id))

@app.route('/')
def index():
    new_task_id = request.args.get('new_task_id')
    tasks = []
    for task_id in TASK_IDS:
        result = AsyncResult(task_id, app=celery_app)
        meta = result.info if result.info else {}
        # Defaults
        progress = total = percent = None
        duration = start_time = end_time = files = None

        if result.state == 'PROGRESS' and isinstance(meta, dict):
            progress = meta.get('current', 0)
            total = meta.get('total', 0)
            percent = int(100 * progress / total) if total else 0
        elif result.state == 'SUCCESS' and isinstance(meta, dict):
            duration = meta.get('duration')
            start_time = meta.get('start_time')
            end_time = meta.get('end_time')
            files = meta.get('files', [])
        tasks.append({
            'id': task_id,
            'state': result.state,
            'progress': progress,
            'total': total,
            'percent': percent,
            'duration': duration,
            'start_time': start_time,
            'end_time': end_time,
            'files': files,
        })
    return render_template_string('''
        <h1>Celery Tasks</h1>
        {% if new_task_id %}
          <p style="color:green;">Started new task: <b>{{ new_task_id }}</b></p>
        {% endif %}
        <form method="post" action="/start">
            <input name="count" type="number" value="10" min="1" max="1000" />
            <button type="submit">Start PDF Task</button>
        </form>
        <table border="1" cellpadding="5">
            <tr>
                <th>Task ID</th>
                <th>Status</th>
                <th>Progress</th>
                <th>Duration (s)</th>
                <th>Start Time</th>
                <th>End Time</th>
            </tr>
            {% for task in tasks %}
            <tr>
                <td>{{task.id}}</td>
                <td>{{task.state}}</td>
                <td>
                    {% if task.progress is not none and task.total %}
                        {{task.progress}} / {{task.total}} ({{task.percent}}%)
                    {% elif task.state == 'SUCCESS' %}
                        Done
                    {% else %}
                        -
                    {% endif %}
                </td>
                <td>
                    {% if task.duration %}
                        {{ "%.2f"|format(task.duration) }}
                    {% elif task.state == 'SUCCESS' %}
                        n/a
                    {% else %}
                        -
                    {% endif %}
                </td>
                <td>
                    {% if task.start_time %}
                        {{task.start_time}}
                    {% else %}
                        -
                    {% endif %}
                </td>
                <td>
                    {% if task.end_time %}
                        {{task.end_time}}
                    {% else %}
                        -
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
        </table>
        <form method="post" action="/add">
            <input name="task_id" placeholder="Add Task ID">
            <button type="submit">Add</button>
        </form>
    ''', tasks=tasks, new_task_id=new_task_id)

@app.route('/add', methods=['POST'])
def add():
    task_id = request.form.get('task_id')
    if task_id and task_id not in TASK_IDS:
        TASK_IDS.append(task_id)
    return '', 302, {'Location': '/'}

if __name__ == '__main__':
    app.run(debug=True)
