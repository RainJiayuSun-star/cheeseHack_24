# Use the official Python 3.9 slim image to minimize image size
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first for dependency installation
COPY requirements.txt requirements.txt

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8080 for Google Cloud Run
EXPOSE 8080

# Command to run the Flask app using gunicorn
CMD ["gunicorn", "-b", ":8080", "app:app"]
