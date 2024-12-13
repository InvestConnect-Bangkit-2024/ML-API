# Use the official Python image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the app will run on
EXPOSE 8080

# Command to run the application using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:7000", "app:app"]