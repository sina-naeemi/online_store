FROM python:3.12-slim

# جلوگیری از cache و بافر
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# نصب وابستگی‌های سیستمی Pillow
RUN apt-get update && apt-get install -y \
    libjpeg-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# کپی requirements
COPY requirement.txt .

# نصب پکیج‌ها
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirement.txt

# کپی کل پروژه (بدون venv)
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]