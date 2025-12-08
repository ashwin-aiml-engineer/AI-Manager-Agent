# 1. The Base Image (The OS)
# We use a lightweight version of Python 3.10
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

ENV ANONYMIZED_TELEMETRY=False
# 3. Install System Dependencies (Required for ChromaDB/Sqlite)
# We install 'build-essential' for compiling C++ libraries and 'curl' for health checks
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy Requirements first (Caching Strategy)
# This way, if you change app.py, Docker won't re-install all pip libraries
COPY requirements.txt .

# 5. Install Python Libraries
RUN pip install --no-cache-dir --default-timeout=1000 -r requirements.txt

# 6. Copy the rest of the application code
COPY . .

# 7. Expose the Port (Streamlit runs on 8501)
EXPOSE 8501

# 8. The Command to run the app
# We use the host networking logic to talk to Ollama
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]