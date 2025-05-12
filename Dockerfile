# Build Stage: 의존성 설치 및 빌드
FROM python:3.11-slim AS build

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    python3-dev \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config

# Install Poetry (Poetry 설치)
RUN pip install --upgrade pip
RUN pip install poetry

# Poetry bin directory to PATH
ENV PATH="/root/.local/bin:$PATH"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory inside the container
WORKDIR /app

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock /app/

# Install dependencies using Poetry (가상환경 사용하지 않음)
RUN poetry config virtualenvs.create false && poetry install --only main --no-root

# Copy the rest of the application files
COPY . /app/

# Production Stage: 최종 실행 환경
FROM python:3.11-slim AS production

ENV PATH="/root/.local/bin:$PATH"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    python3-dev \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    supervisor  # Supervisor for process management in production

# Set working directory inside the container
WORKDIR /app

# Copy installed dependencies from the build stage
COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy the application files from the build stage
COPY --from=build /app /app

# Set Django settings module environment variable
ENV DJANGO_SETTINGS_MODULE=config.settings

# Expose port for Django application
EXPOSE 8000

# Run the Django application using Poetry
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
