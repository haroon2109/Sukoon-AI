# Use the official lightweight Python image.
FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED=True

# Set the working directory
WORKDIR /app

# Create a non-root user
RUN groupadd -r sukoon && useradd -r -g sukoon sukoon

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers, OS dependencies, and ffmpeg
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 && playwright install chromium && playwright install-deps chromium

# Copy the rest of the application code
COPY . .

# Change ownership to the non-root user
RUN chown -R sukoon:sukoon /app

# Switch to the non-root user
USER sukoon

# Expose port
EXPOSE 8000

# Command to run the application using Uvicorn
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
