# Use official Python runtime as a parent image
FROM python:3.10-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
# nmap: required for scanning
# wget, unzip: required for downloading Nuclei
RUN apt-get update && apt-get install -y \
    nmap \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Nuclei
ENV NUCLEI_VERSION=3.3.6
RUN wget https://github.com/projectdiscovery/nuclei/releases/download/v${NUCLEI_VERSION}/nuclei_${NUCLEI_VERSION}_linux_amd64.zip \
    && unzip nuclei_${NUCLEI_VERSION}_linux_amd64.zip \
    && mv nuclei /usr/local/bin/ \
    && rm nuclei_${NUCLEI_VERSION}_linux_amd64.zip

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
