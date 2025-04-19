# Stage 1: Build dependencies
FROM python:3.9-alpine AS builder

# Install build dependencies
RUN apk add --no-cache build-base

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final Image
FROM python:3.9-alpine

# Install gunicorn here if not in requirements.txt
RUN pip install gunicorn

# Copy dependencies from the builder image
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copy app files
COPY app /app

# Print gunicorn location and PATH for debugging
RUN which gunicorn || echo "Gunicorn not found"
RUN pip show gunicorn  # Shows where gunicorn is installed

# Get the gunicorn install location and explicitly check
RUN GUNICORN_PATH=$(pip show gunicorn | grep "Location" | cut -d " " -f 2)/bin && \
    echo "Gunicorn path: $GUNICORN_PATH" && \
    ls -l $GUNICORN_PATH/gunicorn || echo "Gunicorn not found at $GUNICORN_PATH"

# Add the gunicorn installation path to the PATH explicitly
RUN echo "export PATH=$(pip show gunicorn | grep 'Location' | cut -d ' ' -f 2)/bin:$PATH" >> /etc/profile.d/gunicorn.sh
RUN echo "source /etc/profile.d/gunicorn.sh" >> ~/.bashrc

# Create and use a non-root user
RUN addgroup -g 1000 myuser && adduser -u 1000 -G myuser -S myuser

# Set the ownership of files and directories as root before switching to myuser
RUN chown -R myuser:myuser /app

USER myuser

WORKDIR /app

# Expose the required port
EXPOSE 80

# Command to run the application using Gunicorn (for production)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "file_drop:app"]
