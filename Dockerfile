# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxrender1 \
    x11-apps \
    chromium-driver \
    chromium

# Set display port to avoid crash
ENV DISPLAY=:99

# Set up ChromeDriver environment variables
ENV CHROME_BIN=/usr/bin/chromium \
    CHROME_DRIVER=/usr/lib/chromium/chromedriver

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (for Streamlit)
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "demo.py"]
