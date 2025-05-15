# Build Stage
FROM python:3.11-slim AS build

# Set the working directory
WORKDIR /app/

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

ENV POETRY_VERSION=1.2.2

# install poetry to manage python dependencies
RUN curl -sSL https://install.python-poetry.org | python3 -

# install python dependencies
ADD pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --only main --no-root

RUN /root/.local/bin/poetry install --no-root

# copy project
COPY . /app
# run at port 8000
EXPOSE 8000
CMD ["poetry", "run", "python", "manage.py", "runserver"]