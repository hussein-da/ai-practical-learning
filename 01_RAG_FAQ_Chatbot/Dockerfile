# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Using --no-cache-dir to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application script, data directory, and the example environment file
COPY rag_chatbot.py .
COPY data/ ./data/
# Copying env.example.txt for reference; user needs to provide their own .env file when running
COPY env.example.txt .

# Ensure the application runs with UTF-8 encoding (good practice)
ENV PYTHONIOENCODING=UTF-8
ENV LANG=C.UTF-8

# Command to run the application when the container launches
# The user will need to ensure a .env file with their OPENAI_API_KEY is present
# in the /app directory (e.g., by mounting it or using 'docker run --env-file').
CMD ["python", "rag_chatbot.py"] 