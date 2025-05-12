# Step 1: Use an official Python runtime as a parent image
FROM python:3.11-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Install required system dependencies (if needed)
RUN apt-get update && \
    apt-get install -y libpq-dev gcc

# Step 4: Copy the Python dependencies file (requirements.txt)
COPY requirements.txt /app/

# Step 5: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Copy the rest of the application files
COPY .. /app/

# Step 7: Set the environment variable (optional for your use case)
ENV KAFKA_BROKER=kafka:9092

# Step 8: Command to run the Kafka Producer script
CMD ["python", "producer.py"]
