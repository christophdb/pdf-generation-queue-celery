# PDF generation with celery

this is a proof of concept of a python celery queue to generate pdfs with gotenberg.

## How to use:

### Preparation

1. start these containers with `docker compose up -d --build --scale gotenberg=3`
2. monitor the celery logs with `docker compose logs -f`

### Creation tasks

Start your webbrowser and open http://localhost:5000

## Important to know

- one task is operated by one gotenberg. To utilize multiple gotenberg containers, multiple tasks have to be created.

## What to show

- celery takes care of the queue
- gotenberg can generate pdfs really fast
- multiple gotenberg containers can create pdfs even faster