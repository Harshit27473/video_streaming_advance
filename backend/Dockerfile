# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY ./requirements.txt .

# Install any needed packages specified in requirements.txt
# --no-cache-dir: Disables the cache, which is useful for keeping image sizes down.
# --trusted-host: Needed if you are behind a proxy, but good practice for build reliability.
RUN pip install --no-cache-dir  -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . .

EXPOSE 8000

# Command to run the application using uvicorn, making it accessible from outside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]