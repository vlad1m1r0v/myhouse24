<div align="center">

# MyHouse24

**Management system for residential buildings and HOA communities** — a production-grade platform that lets building managers run day-to-day operations and residents manage their accounts online.

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white)](https://redis.io/)
[![Celery](https://img.shields.io/badge/Celery-5.4-37814A?logo=celery&logoColor=white)](https://docs.celeryq.dev/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Nginx](https://img.shields.io/badge/Nginx-Stable-009639?logo=nginx&logoColor=white)](https://nginx.org/)

</div>

---

## About The Project

**MyHouse24** is a web platform for managing multi-apartment residential buildings (HOA / condominium communities). It combines a **public corporate website**, a **resident personal account**, and a **staff/admin back office** in a single Django application.

The system solves a classic HOA problem: scattered records for houses, flats, owners, personal accounts, utility tariffs, meter readings, payment receipts, and cash flow. Managers get one dashboard to track receipts, payments, and master call requests, while residents can view and pay receipts, submit service requests, and message the management team — eliminating paper receipts and phone-call queues.

---

## Key Tech Stack

**Backend**
- **Python 3.11** · **Django 5.1** (MVT)
- **Celery 5.4** — distributed task queue (email verification, password reset, invitations, receipt delivery)
- **Gunicorn 23** — WSGI application server

**Database**
- **PostgreSQL 15** — relational storage
- **django-ajax-datatable** — server-side DataTables integration

**Caching / Message Broker**
- **Redis 7** — Celery broker & result backend

**Frontend / UI**
- **AdminLTE 3** (Bootstrap 4, jQuery, DataTables, Chart.js, CKEditor) — admin panel
- Django templates (server-rendered) + AJAX JSON endpoints

**Document Generation & Integrations**
- **openpyxl** — dynamic Excel receipt/export generation
- **WeasyPrint + xlsx2html** — XLSX → PDF conversion for emailing receipts
- **Pillow** — image handling
- **django-recaptcha** — bot protection on public forms

**DevOps / Deployment**
- **Docker Compose** — 5 services (`web`, `nginx`, `db`, `redis`, `celery`)
- **Nginx** — reverse proxy, static/media serving, 50 MB upload limit
- **Poetry** — dependency & virtualenv management
- **django-environ** — 12-factor environment configuration
- **django-cleanup** — automatic orphan-file cleanup
- **django-debug-toolbar** — development profiling

---

## Core Features

- **Authentication & Role Management**
  - Email-based login (plus login by resident ID number) via a custom `CustomUser` model and custom `EmailBackend`
  - Email verification on registration (async, Celery), password reset, and invitation emails
  - Fine-grained custom permissions per module (`houses`, `flats`, `receipts`, `cash_box`, `statistics`, …) with an admin-side `CustomPermissionRequiredMixin` and a resident-side `OwnerRequiredMixin`
  - 5 predefined staff roles (Director, Manager, Accountant, Electrician, Plumber) bootstrapped by the `creategroups` management command
- **Building Registry** — houses, sections, floors, and flats with photos
- **Flat Owners & Personal Accounts** — owner profiles, invitations, personal accounts with computed balance (`with_balance()` annotation)
- **Tariffs & Services** — service catalog, measurement units, tariffs with per-service prices, payment items (income/expense)
- **Meter Indicators** — meter readings linked to flats and services
- **Payment Receipts**
  - Admin generates receipts from tariff templates; resident sees, downloads (XLSX), prints, and "pays" them online
  - PDF receipts generated (XLSX → HTML → PDF) and **emailed automatically** via Celery
  - Custom `ReceiptManager`/`ReceiptServiceManager` annotate line totals and receipt totals
- **Cash Box** — income/expense transactions per personal account and payment item, Excel export, receipt-linked payments
- **Master Call Requests** — residents submit service requests; staff track them by status
- **User Messages** — broadcast messages to houses/sections/flats/owners with bulk delete
- **Dashboard & Analytics** — admin and resident dashboards with Chart.js charts fed by AJAX endpoints (receipts, cash box, monthly expenses)
- **Public Website** — homepage, about, services, tariffs, contacts (CMS-managed via `website_management`), `sitemap.xml` and `robots.txt`

---

## Architecture & Engineering Highlights

- **Modular monolith** — 14 Django apps under `src/`, each with a consistent `views / forms / models / urls / templates` layout and split URL namespaces (`adminlte`, `account`, `website`), keeping a single deployable unit without microservice overhead.
- **Dual access layer** — the same data model powers three UIs: a public marketing site, a resident personal account, and an AdminLTE back office, with permission enforcement at the view level.
- **ORM optimization** — heavy use of `select_related` / `Prefetch` with annotated `QuerySet`s (e.g., `with_total_price()`, `with_balance()`), `Sum`/`Coalesce`/`F`-expressions to compute totals and paid amounts in the database instead of in Python, and server-side DataTables endpoints so large lists never ship full tables to the browser.
- **Service layer for document generation** — Excel/Pdf generation is isolated into dedicated service classes (`ReceiptExcelService`, `TransactionExcelService`, `AccountExcelService`, `FileConverterService`) that fill branded XLSX templates and convert them to PDF.
- **Asynchronous email pipeline** — all transactional email (verification, resets, invitations, receipt PDFs) is dispatched through Celery with Redis as broker, keeping request cycles fast.
- **Typed, versioned data model** — `AUTH_USER_MODEL = "authentication.CustomUser"` (email + `ID` as alternate identifier), BigAutoField PKs, migrations managed per app (60+ migration files).
- **12-factor config & CI-friendly deploy** — configuration via `.env` (`django-environ`); the web `entrypoint.sh` waits for Postgres, runs `collectstatic`, applies migrations, and seeds roles; Nginx terminates TLS offload boundaries and serves static/media with caching.

---

## Quick Start

### Prerequisites

- **Python 3.11+** and [Poetry](https://python-poetry.org/)
- **Docker** & **Docker Compose** (recommended path)
- **PostgreSQL 15** and **Redis 7** if running locally without Docker

### 1. Clone and configure

```bash
git clone https://github.com/vlad1m1r0v/myhouse24.git
cd myhouse24

cp .env.example .env
```

Fill in `.env` with your values:

```dotenv
SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=myhouse24
DB_USER=myhouse24
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

RECAPTCHA_PUBLIC_KEY=...
RECAPTCHA_PRIVATE_KEY=...

CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=no-reply@example.com
EMAIL_HOST_PASSWORD=...
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
```

### 2. Local setup (without Docker)

```bash
poetry install
poetry shell

python manage.py migrate
python manage.py creategroups          # seed the 5 staff roles
python manage.py createsuperuser       # create your admin
python manage.py runserver
```

App is served at <http://localhost:8000/>.

### 3. Docker Compose (recommended)

```bash
docker compose up --build
```

This starts all five services:

| Service  | Image / Build                 | Exposed port |
|----------|-------------------------------|--------------|
| `web`    | `deploy/web/Dockerfile` (Gunicorn) | `8000`   |
| `nginx`  | `nginx:stable`                | `80`         |
| `db`     | `postgres:15`                 | internal     |
| `redis`  | `redis:7`                     | internal     |
| `celery` | `deploy/celery/Dockerfile`    | internal     |

After the containers are up:

```bash
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py creategroups
```

Open <http://localhost/> — Nginx proxies to the Django app and serves `/static/` and `/media/`.

---

## API Endpoints Overview

The system does not expose a DRF-style REST API; it is a server-rendered application with **AJAX JSON endpoints** (for DataTables grids and dependent dropdowns) plus **document download endpoints**. Key routes:

| Method | Endpoint                                        | Description |
|--------|-------------------------------------------------|-------------|
| POST   | `/authentication/account/register/`             | Resident self-registration (triggers async email verification) |
| POST   | `/authentication/account/login/`                | Login with email or resident ID number |
| GET    | `/adminlte/houses/datatable/`                   | Server-side DataTables listing of houses (AJAX/JSON) |
| GET    | `/account/receipts/{pk}/download/`              | Download a payment receipt as Excel |
| POST   | `/account/receipts/{pk}/pay/`                   | Pay a receipt from the personal-account balance |
| GET    | `/adminlte/cash-box/export/`                    | Export cash-box transactions to Excel |
| GET    | `/adminlte/dashboard/api/receipt-chart/`        | Receipt analytics series for dashboard charts (JSON) |

Additional documentation endpoints:

- **Public site**: `/home/`, `/about-us/`, `/services/`, `/tariffs/`, `/contacts/`
- **SEO**: `/sitemap.xml`, `/robots.txt`
- **Django admin**: `/admin/`

---

## Future Roadmap

1. **Online payment gateway integration** — replace the balance-based "pay" flow with real PSP payments (LiqPay / Fondy) and automatic status reconciliation, plus webhook handling in Celery.
2. **WebSocket-based resident chat** — real-time messaging between residents and management using Django Channels instead of the current request/response message model.
3. **Scheduled billing engine** — a Celery beat cron that auto-generates monthly receipts from tariffs and meter indicators, with an idempotent, transaction-safe generation job and a retry/notification pipeline.

---

## License

License is not specified by the repository owner. All rights reserved by the author.
