# Use lightweight Python base image
FROM python:3.11-slim

# Set the working directory in container
WORKDIR /app

# Copy requirements file first to utilize Docker cache layers
COPY requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app file and serialized model into the container
COPY app.py .
COPY superkart_model.joblib .

# Expose port 7860 which Flask will use
EXPOSE 7860

# Run the Flask app on launch
CMD ["python", "app.py"]