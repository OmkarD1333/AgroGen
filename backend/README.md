# 🌾 AgroGen AI — Backend API

> **High-Performance Asynchronous Agricultural Intelligence Engine**  
> Built with **FastAPI**, **PostgreSQL (SQLAlchemy 2.0)**, **PyTorch / YOLOv8**, and **Google Text-to-Speech (gTTS)**. Designed specifically for bilingual (English & Marathi) smart farming decision support in Maharashtra.

---

## 📑 Table of Contents
- [Architecture Overview](#-architecture-overview)
- [Key Features & Modules](#-key-features--modules)
- [Tech Stack](#-tech-stack)
- [Directory Structure](#-directory-structure)
- [Prerequisites & Setup](#-prerequisites--setup)
- [Environment Variables (.env)](#-environment-variables-env)
- [Database Migrations & Seeding](#-database-migrations--seeding)
- [Running the Application](#-running-the-application)
- [API Documentation & Endpoints](#-api-documentation--endpoints)
- [Testing](#-testing)

---

## 🏛 Architecture Overview

AgroGen AI Backend is an enterprise-grade REST API powering real-time crop disease diagnosis, agro-meteorological forecasting, mandi market price analytics, government scheme eligibility checks, and Marathi voice synthesis.

```
       +---------------------------------------------+
       |             React / Vite Frontend           |
       +---------------------------------------------+
                              |
                     HTTPS / JSON / JWT
                              v
       +---------------------------------------------+
       |             FastAPI ASGI Server             |
       |               (Uvicorn + CORS)              |
       +---------------------------------------------+
                              |
      +-----------------------+-----------------------+
      |                       |                       |
      v                       v                       v
[ Auth & Core ]        [ AI Vision & Audio ]    [ DB & Analytics ]
- JWT (OAuth2)         - YOLOv8 Inference       - SQLAlchemy 2.0
- Pydantic v2          - PyTorch (CUDA)         - PostgreSQL / Supabase
- Role Guard           - gTTS (Marathi/English) - Alembic Migrations
```

---

## 🚀 Key Features & Modules

1. **Authentication & Profile Management (`/api/auth`, `/api/farmer`)**
   - Secure farmer registration, login, and JWT bearer token issuance.
   - Farm profile tracking (land size in acres, soil type, district/taluka, irrigation facilities).
2. **AI Crop Disease Diagnosis (`/api/disease`)**
   - Leaf image upload pipeline with validation.
   - Deep learning computer vision inference (YOLOv8) returning disease name, confidence score, and specific pesticide/cultural treatments.
3. **Agro-Weather Advisory (`/api/weather`)**
   - OpenWeather integration with tailored farming advisories (spraying advisories, frost warnings, rain impact).
4. **Mandi Market Prices (`/api/market`)**
   - APMC mandi commodity prices across Maharashtra districts with min, max, and modal rates.
5. **Government Schemes (`/api/schemes`)**
   - Central and Maharashtra state agricultural subsidies and welfare schemes with eligibility verification.
6. **Voice Synthesis (`/api/voice`)**
   - Converts agricultural advisories into spoken Marathi (`mr`) or English (`en`) audio files using `gTTS`.
7. **Crop Yield Prediction (`/api/yield`)**
   - Calculates estimated yield per acre based on crop variety, soil profile, seasonal rainfall, and fertilizer usage.
8. **Automated Agricultural Recommendations (`/api/recommendations`)**
   - Context-aware daily/weekly task schedules for farmers based on their active crop cycles.

---

## 🛠 Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+)
- **ASGI Server:** [Uvicorn](https://www.uvicorn.org/)
- **Database ORM:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (Async-ready Declarative Models)
- **Database Driver:** `psycopg[binary]` (PostgreSQL / Supabase)
- **Data Validation:** [Pydantic v2](https://docs.pydantic.dev/) + `pydantic-settings`
- **Schema Migrations:** [Alembic](https://alembic.sqlalchemy.org/)
- **Deep Learning / Vision:** [PyTorch](https://pytorch.org/) (CUDA 12.4 supported), [Ultralytics YOLOv8](https://docs.ultralytics.com/)
- **Voice Synthesis:** [gTTS](https://gtts.readthedocs.io/) (Google Text-to-Speech)
- **Image Processing:** Pillow & OpenCV (`opencv-python`)

---

## 📁 Directory Structure

```
backend/
├── alembic/                 # Database migration environments & revisions
│   ├── versions/            # Migration version scripts
│   └── env.py               # Alembic database environment hook
├── app/
│   ├── api/                 # Modular API route controllers
│   │   ├── auth.py          # /api/auth (Login, Register)
│   │   ├── farmer.py        # /api/farmer (Farmer Profile)
│   │   ├── crops.py         # /api/crops (Crop management)
│   │   ├── disease.py       # /api/disease (Leaf image diagnosis)
│   │   ├── weather.py       # /api/weather (Weather forecasts)
│   │   ├── market.py        # /api/market (Mandi prices)
│   │   ├── schemes.py       # /api/schemes (Govt. schemes)
│   │   ├── chatbot.py       # /api/chatbot (Advisory chat)
│   │   ├── voice.py         # /api/voice (Marathi TTS audio)
│   │   ├── yield_prediction.py # /api/yield (Yield calculation)
│   │   ├── recommendations.py # /api/recommendations (Actionable advice)
│   │   └── notifications.py # /api/notifications (Farmer alerts)
│   ├── core/                # Core configurations
│   │   ├── config.py        # Pydantic Settings & .env loading
│   │   ├── database.py      # SQLAlchemy engine & session factory
│   │   ├── security.py      # Password hashing (bcrypt) & JWT tokens
│   │   └── logging.py       # Centralized app logging
│   ├── dependencies/        # FastAPI Depends helpers (auth, DB session)
│   ├── models/              # SQLAlchemy ORM database models
│   ├── schemas/             # Pydantic request/response schemas (DTOs)
│   ├── services/            # Business logic layer
│   └── main.py              # Application entry point & router mounting
├── scripts/                 # Standalone administrative scripts
│   ├── create_tables.py     # Direct DB table initialization
│   └── seed_data.py         # Seed demo crops, schemes, and market prices
├── tests/                   # Pytest test suite
│   ├── unit/                # Unit tests for services and schemas
│   └── integration/         # Integration tests for DB and API endpoints
├── uploads/                 # Local media storage (git-ignored)
│   ├── audio/               # Generated speech audio files (.mp3)
│   └── disease/             # Uploaded crop leaf images for diagnosis
├── .env.example             # Template for environment secrets
├── requirements.txt         # Production and development dependencies
└── README.md                # Backend documentation
```

---

## ⚙️ Prerequisites & Setup

### 1. Python Environment
Make sure you are using Python 3.10+ and activate your project virtual environment:

```powershell
# From project root:
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```powershell
pip install -r backend/requirements.txt
```

---

## 🔐 Environment Variables (.env)

Create a `.env` file inside `backend/` by copying `.env.example`:

```powershell
cp backend/.env.example backend/.env
```

Fill in the required configuration:

```ini
# PostgreSQL connection string (Supabase / local Postgres)
DATABASE_URL=postgresql://postgres.xxx:YOUR_PASSWORD@aws-0-ap-south-1.pooler.supabase.com:6543/postgres

# JWT Secret & Expiry
SECRET_KEY=your-super-secret-random-32-byte-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# AI & Weather API Keys
GEMINI_API_KEY=your-google-gemini-api-key
OPENWEATHER_API_KEY=your-openweather-api-key

# App Settings
DEBUG=False
APP_NAME=AgroGen AI
APP_VERSION=1.0.0

# CORS Allowed Origins
ALLOWED_ORIGINS=["http://localhost:5173","http://localhost:3000"]
```

---

## 🗄 Database Migrations & Seeding

### 1. Initialize Database Tables
You can generate tables using SQLAlchemy declarative metadata:
```powershell
# From project root
python backend/scripts/create_tables.py
```

Or using Alembic migrations:
```powershell
cd backend
alembic upgrade head
```

### 2. Seed Initial Demo Data
Populate standard crops, APMC mandi rates, and Maharashtra government agricultural schemes:
```powershell
python backend/scripts/seed_data.py
```

---

## 🚀 Running the Application

### Development Server (with auto-reload)
Run from the `backend/` directory:
```powershell
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Or execute directly with Python:
```powershell
python app/main.py
```

The server will start at: `http://localhost:8000`

---

## 📖 API Documentation & Endpoints

FastAPI automatically generates interactive OpenAPI/Swagger documentation:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc UI:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health Check:** [http://localhost:8000/health](http://localhost:8000/health)

### Primary Endpoint Routes

| HTTP Method | Route | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/register` | Register a new farmer account | No |
| `POST` | `/api/auth/login` | Login and obtain JWT access token | No |
| `GET` / `PUT` | `/api/farmer/profile` | View or update farmer profile & land info | Yes (Bearer) |
| `GET` / `POST` | `/api/crops/` | Manage farmer's active cultivated crops | Yes (Bearer) |
| `POST` | `/api/disease/detect/{crop_id}` | Upload leaf photo & run AI disease detection | Yes (Bearer) |
| `GET` | `/api/weather/forecast` | Current & 7-day agro-weather forecast | Yes (Bearer) |
| `GET` | `/api/market/prices` | APMC mandi commodity rates by district | No |
| `GET` | `/api/schemes/` | View eligible Maharashtra govt. subsidies | No |
| `POST` | `/api/yield/predict` | Calculate expected crop yield & revenue | Yes (Bearer) |
| `POST` | `/api/voice/synthesize` | Convert advisory text to Marathi/English MP3 | Yes (Bearer) |
| `GET` | `/uploads/{path}` | Static file server for uploaded leaves & audio | No |

---

## 🧪 Testing

Run unit and integration tests using `pytest`:

```powershell
# Run all tests
pytest backend/tests

# Run unit tests only
pytest backend/tests/unit

# Run tests with coverage report
pytest backend/tests --cov=backend/app
```
