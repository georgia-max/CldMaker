# Use an official Python runtime as a parent image
FROM python:3.11

RUN apt-get update \
    && apt-get install -y \
    cmake \
    freetds-dev \
    g++ \
    gcc \
    tar \
    gfortran \
    gnupg \
    libffi-dev \
    libpng-dev

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt

# Define environment variable
ENV FLASK_APP=main.py
ENV FLASK_ENV=development
ENV FLASK_RUN_PORT=5000
ENV FLASK_RUN_HOST=0.0.0.0
# Make port 5000 available to the world outside this container
EXPOSE 5000


# Run app.py when the container launches
CMD ["flask", "run"]
