# Use the official Python 3.9 slim image as the base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file to leverage Docker's caching
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8080 for Google Cloud Run
EXPOSE 8080

# Command to run the Flask app using gunicorn
CMD ["gunicorn", "-b", ":8080", "app:app"]
