# ----------- Stage 1: Build dependencies ------------
FROM python:3.13-alpine AS builder

# Install compiler and build dependencies
RUN apk add --no-cache build-base libffi-dev

# Upgrade pip/setuptools to fix CVEs
RUN pip install --no-cache-dir --upgrade pip setuptools

# Set working directory
WORKDIR /app

# Copy dependency list and install it (gunicorn should be here)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ----------- Stage 2: Final runtime image ------------
FROM python:3.13-alpine

# Set working directory
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.13 /usr/local/lib/python3.13
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy app code
COPY app /app

# Create a non-root user and own app directory
RUN addgroup -g 1000 myuser && \
    adduser -u 1000 -G myuser -S myuser && \
    chown -R myuser:myuser /app

USER myuser

# Expose port and define command
EXPOSE 80
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "file_drop:app"]
