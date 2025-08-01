FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y build-essential

# Установка рабочей директории
WORKDIR /app

# Копирование зависимостей и установка
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего проекта
COPY . .

# Команда запуска FastAPI-приложения через Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
