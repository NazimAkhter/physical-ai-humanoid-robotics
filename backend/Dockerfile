# Use Python 3.10 for compatibility with HF Spaces
FROM python:3.10

# Create non-root user with UID 1000 (required by HF Spaces)
RUN useradd -m -u 1000 user

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies (as root, with proper ownership)
COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy application code (with proper ownership)
COPY --chown=user:user . .

# Switch to non-root user
USER user

# Set environment variables
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

# Expose port 7860 (documentation only)
EXPOSE 7860

# Run application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
