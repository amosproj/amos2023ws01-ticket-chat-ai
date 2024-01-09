# Use the official Python base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt -q

# Copy the rest of the application source code into the container
COPY app app
COPY config.ini config.ini
COPY config.py config.py

# Expose the port that the FastAPI service will use (default is 8000)
EXPOSE 8000

# Start the api service and the email proxy when the container starts
CMD uvicorn app.main:app --host 0.0.0.0 --port 8000 & python app/email/main.py