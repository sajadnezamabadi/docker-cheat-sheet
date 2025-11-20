FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY demo.py .

# Create non-root user
RUN useradd -m -u 1000 pgapp && \
    chown -R pgapp:pgapp /app

USER pgapp

EXPOSE 5000

CMD ["python", "demo.py"]

