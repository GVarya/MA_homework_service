# FROM python:3.10

# # Установка системных зависимостей (если нужны)
# RUN apt-get update && apt-get install -y \
#     curl \
#     && rm -rf /var/lib/apt/lists/*

# # Устанавливаем рабочую директорию
# WORKDIR /app

# # Копируем файл с зависимостями
# COPY requirements.txt .

# # Устанавливаем зависимости
# RUN pip install --no-cache-dir --upgrade -r requirements.txt

# # Копируем проект
# COPY ./app ./app

# # Команда запуска
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.10
WORKDIR /code
RUN ls
COPY ./requirements.txt /code/
RUN pip install -r requirements.txt
COPY app /code/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]