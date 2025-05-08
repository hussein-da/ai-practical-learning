# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=app.py
# Set the default port (can be overridden by PORT env var at runtime)
ENV PORT 5000 

# Set the working directory in the container
WORKDIR /app

# Install system dependencies if needed (e.g., for certain ML libraries)
# RUN apt-get update && apt-get install -y --no-install-recommends some-package && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
# We use --no-cache-dir to reduce image size
# Using torch's CPU-only version can significantly reduce image size if GPU is not needed
# Consider adding `--index-url https://download.pytorch.org/whl/cpu` to the pip install command
# if you only need the CPU version of PyTorch.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run the application using waitress
# Waitress is a production-quality WSGI server
CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "app:app"] 