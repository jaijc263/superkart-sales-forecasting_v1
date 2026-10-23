# Use lightweight Python base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements file first to utilize Docker cache layers
COPY requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Streamlit application into the container
COPY app_frontend.py .

# Expose port 8501 which Streamlit uses by default
EXPOSE 8501

# Run the Streamlit app on launch
CMD ["streamlit", "run", "app_frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]