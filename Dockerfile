# Use an official Python image
FROM python:3.10-slim

# Install Chromium and dependencies
RUN apt-get update && \
    apt-get install -y chromium chromium-driver && \
    apt-get clean

# Set environment variable so Selenium can find Chrome
ENV CHROME_BINARY=/usr/bin/chromium

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 10000

# Start your app with gunicorn
CMD ["gunicorn", "scraper_api:app", "--bind", "0.0.0.0:10000"]