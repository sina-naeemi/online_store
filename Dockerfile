FROM python:3.12-slim

# جلوگیری از cache و بافر
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

# نصب وابستگی های سیستمی و پایگاه داده
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# کپی requirements
COPY requirement.txt .

# نصب پکیج‌ها
RUN pip install --upgrade pip
RUN pip install -r requirement.txt

# کپی کل پروژه (بدون venv)
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]