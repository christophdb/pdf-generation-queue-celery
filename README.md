# PDF generation with celery

this is a proof of concept of a python celery queue to generate pdfs with gotenberg.

## How to use:

### Preparation

1. start these containers with `docker compose up -d --build --scale gotenberg=3`
2. monitor the celery logs with `docker compose logs -f`

### Creation tasks

Start your webbrowser and open http://localhost:5000

## Results

### 5x20 PDFs with one gotenberg - started in parallel **

```
Task ID	Status	Progress	Duration (s)	Start Time	End Time
4f62a1ad-3b42-4318-b7bb-eb33f523151b	SUCCESS	Done	15.19	2025-07-03T13:44:12.149316	2025-07-03T13:44:27.342055
4145184b-d5a7-49d4-9c38-819777104a5b	SUCCESS	Done	15.39	2025-07-03T13:44:12.652476	2025-07-03T13:44:28.045561
bf4dff46-dbee-42bf-b3a3-4638080fd14d	SUCCESS	Done	15.92	2025-07-03T13:44:13.065181	2025-07-03T13:44:28.982442
dd60222f-a415-45f0-9969-93a54f46ed1c	SUCCESS	Done	15.85	2025-07-03T13:44:13.443536	2025-07-03T13:44:29.297772
c4e42ce1-601e-462c-b99a-e3d698d27ccf	SUCCESS	Done	15.68	2025-07-03T13:44:13.782591	2025-07-03T13:44:29.467206
```

### 5x20 PDFs with three gotenbergs - started in parallel **

```
f7365e73-a7b5-425a-96c7-b67005c25171	SUCCESS	Done	10.68	2025-07-03T13:45:00.045805	2025-07-03T13:45:10.727485
da311c40-9f8f-4b4c-ba8a-f98cfd2b9d0d	SUCCESS	Done	7.58	2025-07-03T13:45:00.530873	2025-07-03T13:45:08.111470
0f3ebb3b-df44-400b-9082-3eeafecd0346	SUCCESS	Done	9.79	2025-07-03T13:45:00.941364	2025-07-03T13:45:10.730781
005c8169-19e0-41e1-9e86-996185417bb6	SUCCESS	Done	10.69	2025-07-03T13:45:01.324081	2025-07-03T13:45:12.015405
93cbaecd-d2a0-4d32-aca1-1e6310b33076	SUCCESS	Done	9.75	2025-07-03T13:45:01.682404	2025-07-03T13:45:11.428655
```

### 5x20 PDFs with five gotenbergs - started in parallel **

```
869cae19-8066-41f2-b7e2-86c7c628a91c	SUCCESS	Done	9.15	2025-07-03T13:45:37.928637	2025-07-03T13:45:47.077466
5e7657d2-bf2b-46b6-bd09-f1864974c852	SUCCESS	Done	9.31	2025-07-03T13:45:38.490474	2025-07-03T13:45:47.803292
ed5b0476-cd64-46d5-82a0-bce4baeda394	SUCCESS	Done	8.65	2025-07-03T13:45:38.858642	2025-07-03T13:45:47.508029
a0db44eb-61f3-4b9c-b831-a5a2a24d996f	SUCCESS	Done	8.63	2025-07-03T13:45:39.190558	2025-07-03T13:45:47.816460
86ab71f6-f8af-43f6-bd04-63455549188b	SUCCESS	Done	8.45	2025-07-03T13:45:39.588933	2025-07-03T13:45:48.036548
```

## Important to know

- one task is operated by one gotenberg. To utilize multiple gotenberg containers, multiple tasks have to be created.

## What to show

- celery takes care of the queue
- gotenberg can generate pdfs really fast
- multiple gotenberg containers can create pdfs even faster