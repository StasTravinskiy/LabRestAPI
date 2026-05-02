FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Використовуємо шлях app.main:app, оскільки робоча директорія /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]