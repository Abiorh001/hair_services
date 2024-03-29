# Use the official Python slim image
FROM python:3.11.6-slim-bullseye


# Create working directory
WORKDIR /hairsol_backend

# Copy local files to the container
COPY . /hairsol_backend

# Install Python dependencies from requirements.txt if it exists
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
