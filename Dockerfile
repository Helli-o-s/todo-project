# Use an official lightweight Python image as a parent image
FROM python:3.9-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# --no-cache-dir makes the image smaller
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container at /app
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables for Flask
ENV FLASK_APP=app.py

# Run the app. The --host=0.0.0.0 makes the server accessible
# from outside the container. This is crucial.
CMD ["flask", "run", "--host=0.0.0.0"]