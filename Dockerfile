# Use a Python base image
FROM python:3.10-slim

# Set environment variables to prevent Python from buffering output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file to leverage Docker's caching
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . /app/

# Expose the port that Flask will run on
EXPOSE 5000

# Command to run the Flask app using Gunicorn (a production-grade WSGI server)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]

