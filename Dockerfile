FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

RUN chmod +x /app/start.sh

# Create instance directory and set permissions
RUN mkdir -p /app/instance && chmod 777 /app/instance

# Create products images directory and set permissions
RUN mkdir -p /app/app/static/images/products && chmod 777 /app/app/static/images && chmod 777 /app/app/static/images/products

# Expose port
EXPOSE 5000

# Environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

# Run the startup script (which seeds DB then starts app)
CMD ["/app/start.sh"]
