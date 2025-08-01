FROM python:3.11-slim

# Установка необходимых инструментов для сборки
RUN apt-get update && apt-get install -y build-essential

# Копирование файла requirements.txt в контейнер
COPY requirements.txt /app/

# Установка зависимостей
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копирование остальных файлов проекта
COPY . /app

# Установка рабочей директории
WORKDIR /app

COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Команда по умолчанию
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

