# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Prevent Python from writing pyc files to disc (optional)
ENV PYTHONDONTWRITEBYTECODE 1
# Ensure Python output is sent straight to terminal (recommended for logs)
ENV PYTHONUNBUFFERED 1

# Install system dependencies that might be needed by some ML libraries (optional, add as needed)
# RUN apt-get update && apt-get install -y --no-install-recommends some-package && rm -rf /var/lib/apt/lists/*

# Install pip requirements
# Copy only requirements first to leverage Docker layer caching
COPY ./sentiment_api/requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY ./sentiment_api /app/

# Expose the port the app runs on
EXPOSE 8000

# Define the command to run the application
# Use 0.0.0.0 to make it accessible from outside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 