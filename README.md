# AI Health Prediction

AI Health Prediction is a full-stack health assessment application built with FastAPI, PostgreSQL, Groq AI, and a lightweight HTML/CSS/JavaScript interface. It stores patient records and generates educational health remarks from glucose, haemoglobin, and cholesterol values.

> This application provides AI-assisted educational information only. It does not confirm a diagnosis or replace professional medical advice.

## Features

- Create, view, edit, search, and delete patient records
- Validate patient details and blood values
- Generate Groq AI health remarks for blood test values
- Run in demo mode without an API key
- Persist data with PostgreSQL
- Run locally or with Docker Compose
- Swagger API documentation

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Groq API
- Uvicorn
- Docker and Docker Compose
- HTML, CSS, and JavaScript

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Web interface |
| GET | `/api/health` | Application and AI mode status |
| POST | `/api/patients` | Create a patient record |
| GET | `/api/patients` | List patient records |
| GET | `/api/patients/{id}` | Get a patient record |
| PUT | `/api/patients/{id}` | Update a patient record |
| DELETE | `/api/patients/{id}` | Delete a patient record |
| GET | `/docs` | Swagger UI |

## Prerequisites

- Python 3.11+
- PostgreSQL
- Docker and Docker Compose (for the container setup)
- A Groq API key (optional for demo mode)

## Environment Configuration

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/health_prediction_db
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
AI_MODE=live
POSTGRES_PASSWORD=postgres
```

Set `AI_MODE=mock` to use demo mode. Demo mode does not call Groq and returns:

```text
DEMO MODE: AI prediction not performed.
```

## Run with Docker Compose

```powershell
docker compose up --build
```

Open:

- Application: http://localhost:8000
- API documentation: http://localhost:8000/docs

Stop the containers:

```powershell
docker compose down
```

To remove the database volume as well:

```powershell
docker compose down -v
```

## Run Locally

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create a PostgreSQL database and configure `DATABASE_URL` in `.env`.

Start the application:

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000.

## Run Tests

```powershell
pytest
```

## Project Structure

```text
app/
  ai_service.py  Groq integration
  config.py      Environment configuration
  crud.py        Database operations
  database.py    SQLAlchemy setup
  main.py        FastAPI application and routes
  models.py      Database models
  schemas.py     Pydantic request and response models
static/
  index.html     Web interface
  script.js      Frontend behavior
  style.css      Styles
tests/
Dockerfile
docker-compose.yml
requirements.txt
```

## Security Notes

- Keep `.env`, database passwords, and API keys out of source control.
- Configure Groq credentials only through environment variables.
- The current application is intended for development and educational use.