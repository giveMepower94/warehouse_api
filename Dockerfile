FROM python:3.11-slim

# Системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Отключаем создание виртуального окружения Poetry
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_VIRTUALENVS_IN_PROJECT=false

WORKDIR /app

# Копируем только файлы poetry, чтобы быстрее собирать образ
COPY pyproject.toml poetry.lock* /app/

# Poetry не создаёт виртуальные окружения
RUN poetry config virtualenvs.create false \
 && poetry config virtualenvs.in-project false

# Устанавливаем зависимости
RUN poetry install --no-root --no-interaction --no-ansi

# Копируем весь проект
COPY . /app/

# Копируем .env
COPY .env /app/.env

EXPOSE 8000

# Запуск Django через gunicorn
CMD ["poetry", "run", "gunicorn", "warehouse.wsgi:application", "--bind", "0.0.0.0:8000"]