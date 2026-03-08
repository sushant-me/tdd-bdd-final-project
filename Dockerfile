# Stage 1: Build stage
# Use a full python image to install dependencies
FROM python:3.9-slim AS builder

# Create a working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage
# Use a smaller footprint for the final image
FROM python:3.9-slim--no-install-recommends

WORKDIR /app

# Copy only the installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the application code
COPY . .

# Create a non-privileged user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "wsgi:app"]
