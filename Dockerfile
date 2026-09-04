# Use a standard Python environment
FROM python:3.10-slim

# Install Linux audio drivers for the voice engine
RUN apt-get update && apt-get install -y espeak

# Set the working folder
WORKDIR /app

# Copy your ingredient list and install them
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy all your code and the AI brain into the cloud computer
COPY . .

# Expose the port FastAPI uses
EXPOSE 8000

# Command to wake up the server
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]