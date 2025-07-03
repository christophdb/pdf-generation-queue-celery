# PDF generation with celery

TODO: what is this...

## How to use:

### Preparation

1. start these containers with `docker compose up -d`
2. monitor the celery logs with `docker compose logs -f`

### Creation tasks

Enter the container with `docker exec -it worker bash` and execute these commands:

- `python3 submit_task.py`
- `python3 check_result.py <task-id>`
