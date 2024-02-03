FROM python:3.11

WORKDIR /app

# Копируем только requirements.txt в корень контейнера
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt --no-cache-dir

# Копируем остальное содержимое проекта
COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "alpharoute.wsgi"]