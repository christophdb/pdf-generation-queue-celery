FROM python:3.11-slim

# Create a user with UID 1000
RUN useradd -u 1000 -ms /bin/bash workeruser

# Set work directory
WORKDIR /app

# Install system utilities
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        nano \
        curl \
        vim \
        less \
        iputils-ping \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Switch to the new user
USER 1000

# Keep the container running and allow interactive shell access
#CMD ["tail", "-f", "/dev/null"]
CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]
