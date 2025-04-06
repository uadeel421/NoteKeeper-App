FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 5000 for the Flask application
EXPOSE 5000

# Start the Flask application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
