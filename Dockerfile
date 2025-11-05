# Base image
FROM python:3.13-slim

# Set work directory
WORKDIR /app

# Copy local files to container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir flask paramiko

# Expose SSH port
EXPOSE 22

# Run honeypot app
CMD ["python", "app.py"]
