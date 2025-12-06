FROM python:3.11-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Добавляем Poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

# Рабочая директория
WORKDIR /app

# Копируем файлы Poetry
COPY pyproject.toml poetry.lock* /app/

# Poetry без виртуальных окружений
RUN poetry config virtualenvs.create false

# Установка зависимостей
RUN poetry install --no-interaction --no-ansi

# Копируем код проекта
COPY . /app/

EXPOSE 8000

CMD ["poetry", "run", "gunicorn", "warehouse_api.wsgi:application", "--bind", "0.0.0.0:8000"]