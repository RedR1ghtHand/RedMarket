FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set workdir
WORKDIR /app

# Install dependencies
RUN apt-get update \
    && apt-get install -y \
        curl \
        build-essential \
        libpq-dev \
        netcat-openbsd \
    && pip install --upgrade pip \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml poetry.lock ./
ENV POETRY_VIRTUALENVS_IN_PROJECT=false
RUN poetry install --no-root

# Copy the rest of the project
COPY . ./

# Copy entrypoint script
COPY docker/python/setup.sh /

RUN poetry run python manage.py collectstatic --noinput

RUN chmod +x /setup.sh

ENTRYPOINT ["/setup.sh"]

EXPOSE 8000

CMD ["poetry", "run", "gunicorn", "redmarket.wsgi:application", "--bind", "0.0.0.0:8000"]
