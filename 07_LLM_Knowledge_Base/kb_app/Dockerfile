# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies if needed (unlikely for this app, but good practice)
# RUN apt-get update && apt-get install -y --no-install-recommends some-package && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
# Using --no-cache-dir reduces image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
# This includes app.py and the data/ directory
COPY . .

# Expose the port Streamlit runs on (default is 8501)
EXPOSE 8501

# Healthcheck (optional but recommended)
# Checks if the Streamlit server is responding
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Define the command to run the Streamlit application
# Uses the standard Streamlit command
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"] 