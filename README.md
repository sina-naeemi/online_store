# Online Store API

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.2-darkgreen?logo=django)
![Django REST Framework](https://img.shields.io/badge/Django%20REST%20Framework-DRF-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?logo=postgresql)
![Docker Compose](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)
![JWT](https://img.shields.io/badge/JWT-simplejwt-orange)
![Swagger](https://img.shields.io/badge/Swagger-drf--spectacular-85EA2D?logo=swagger)

A RESTful API for a digital products store — built with Django REST Framework. Uses passwordless email OTP authentication, JWT-based authorization, subscription-based content access, and payment gateway integration.

## Setup (Docker)

```bash
git clone https://github.com/sina-naeemi/online_store.git
cd online_store
cp .env.example .env   # fill in your values, see below
docker compose build
docker compose up -d
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```
API available at `http://localhost:8000/`, interactive docs at `http://localhost:8000/api/docs/`.

## Setup (without Docker)

```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirement.txt
cp .env.example .env   # set DB_HOST=localhost, fill in the rest
python manage.py migrate
python manage.py runserver
```

## Environment Variables

See `.env.example` for the full list. Key ones:
- `SECRET_KEY` — generate your own, don't reuse a shared one
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` — PostgreSQL credentials
- `GMAIL_USER`, `GMAIL_APP_PASSWORD` — Gmail [App Password](https://myaccount.google.com/apppasswords) used to send OTP emails

> Sending email requires an open outbound SMTP connection (port 587). Some local networks block this — a VPN may be needed for local testing only; not an issue on a real server/host.

## Authentication Flow

No passwords — login is email + OTP:

1. `POST /account/enter/` — `{ "email", "phone_number" }` → creates the user if new, emails a 5-digit code (valid 2 min)
2. `POST /verify-otp/` — `{ "email", "code" }` → returns `access` and `refresh` JWT tokens
3. `POST /token/refresh/` — `{ "refresh" }` → returns a new `access` token

Use the token on protected endpoints:
```
Authorization: Bearer <access_token>
```

## Project Structure

```
User/            → auth, accounts, profiles
products/        → catalog, categories, files
subscriptions/   → plans & active subscriptions
peyments/        → gateways & transactions
digital_product/ → settings, root urls
``` 
