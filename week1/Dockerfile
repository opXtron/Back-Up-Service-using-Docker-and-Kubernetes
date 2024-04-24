# Use an official Python runtime as a base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the client secret file into the container at /app
COPY client_secret.json /app/

# Copy the backup service script into the container at /app
COPY demo.py /app/

COPY token.pickle /app/

COPY upload /app/upload
# Run combined_script.py when the container launches
CMD ["python", "./demo.py"]

