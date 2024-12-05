# Base image with Python
FROM python:3.12

ENV PYTHONUNBUFFERED=1
# Install system dependencies and Java
RUN apt-get update && apt-get install -y \
    default-jre-headless \        
    ghostscript \                 
    python3-tk \                  
    libxml2-dev \                 
    libxslt-dev \                 
    libz-dev \                    
    libjpeg-dev \                 
    gcc \                         
    build-essential \             
    poppler-utils \               
    && rm -rf /var/lib/apt/lists/*  

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Set working directory
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose application port
EXPOSE 5002

# Run the application
CMD ["python", "run.py"]
