# Base image
FROM python:3.11-slim

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set Poetry bin directory to PATH
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock /app/

# Install dependencies using Poetry
RUN poetry install --no-dev

# Copy the rest of the application code
COPY . /app/

# Set the environment variable for .env file location
ENV DJANGO_SETTINGS_MODULE=config.settings

# Expose the port for Django
EXPOSE 8000

# Command to run the Django application
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
