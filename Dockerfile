# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt first
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install netcat-openbsd
RUN apt-get update && apt-get install -y netcat-openbsd

# Copy the entire project directory into the container
COPY . /app

# Copy the initialization script
COPY init.sh /app/

# Make the initialization script executable
RUN chmod +x /app/init.sh

# Expose the port that app runs on
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV ENVIRONMENT=docker

# Set the command to run when the container starts
CMD ["/app/init.sh"]
