# Dockerfile to build a flask app

FROM python:3.10.13-bullseye

# Set the working directory to /app

WORKDIR /app

# Copy the current directory contents into the container at /app

COPY . .

# Install any needed packages specified in requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container

EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host", "0.0.0.0"]