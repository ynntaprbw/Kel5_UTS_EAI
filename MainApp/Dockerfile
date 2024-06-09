FROM python:3.10.7-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Install pkg-config
RUN apt-get update && apt-get install -y pkg-config

# Copy project files ke working directory
COPY . /app/

# Expose port yang digunakan oleh aplikasi Flask
EXPOSE 5000

# Jalankan aplikasi Flask
CMD ["python", "app.py"]