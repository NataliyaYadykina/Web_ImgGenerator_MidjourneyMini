# Используем базовый образ Python
FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем Flask для запуска на порту 5000
EXPOSE 5000

# Запуск приложения
ENTRYPOINT ["sh", "docker-entrypoint.sh"]
