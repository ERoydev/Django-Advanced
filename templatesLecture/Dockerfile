# Base Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Install supervisord
RUN apt-get update && apt-get install -y supervisor && apt-get clean

# Expose port 8000 for Django
EXPOSE 8000

# Copy supervisord configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Default command runs supervisord
CMD ["supervisord", "-n", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
