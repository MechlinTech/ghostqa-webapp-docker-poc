# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIPENV_VERBOSITY=-1

# Set work directory
WORKDIR /app

RUN apt-get update \
    && apt-get install -y docker.io

# Install pipenv
RUN pip install --upgrade pip && \
    pip install pipenv

# Install dependencies
COPY Pipfile Pipfile.lock /app/
RUN pipenv install --system --deploy --ignore-pipfile

# Copy project
COPY ./ghostqa/ /app/

# Expose port
EXPOSE 8000

# Run the application
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
