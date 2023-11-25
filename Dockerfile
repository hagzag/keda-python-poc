# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install Poetry
RUN pip install poetry

# Copy the project files (pyproject.toml and poetry.lock) into the working directory
COPY pyproject.toml poetry.lock* /usr/src/app/

# Install project dependencies
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

# Copy the content of the local src directory to the working directory
COPY . /usr/src/app

# Specify the command to run on container start
CMD [ "poetry", "run", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5000"]
