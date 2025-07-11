# Base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /receipe_management_system

# Install system dependencies
RUN apt-get update && apt-get install -y netcat-openbsd gcc libpq-dev

# Install Python dependencies
COPY requirements.txt /receipe_management_system/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all files, including entrypoint
COPY . /receipe_management_system/

# Make entrypoint executable
RUN chmod +x /receipe_management_system/entrypoint.sh

# Expose port
EXPOSE 8000

# Entrypoint script
CMD ["sh", "/receipe_management_system/entrypoint.sh"]