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
# Install system dependencies
RUN apt-get update \
    && apt-get install -y \
        build-essential \
        libpq-dev \
        postgresql-client \
        netcat

# Install dependencies
COPY Pipfile Pipfile.lock /app/
RUN pipenv install --system --deploy --ignore-pipfile
RUN pipenv install gunicorn

# Copy project
COPY ./ghostqa/ /app/

CMD python manage.py collectstatic


# Expose port
EXPOSE 8000



# Run the application
# CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["pipenv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "ghostqa.wsgi:application"]