from contextlib import asynccontextmanager

from fastapi import (
    FastAPI,
    Depends,
    HTTPException
)

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.config import BASE_DIR, AI_MODE
from app.database import Base, engine, get_db
from app.schemas import PatientCreate, PatientResponse

from app import crud, models

from app.ai_service import (
    generate_health_remarks,
    AIServiceError
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    Base.metadata.create_all(bind=engine)

    yield


app = FastAPI(
    title="AI Health Prediction API",
    version="1.0.0",
    lifespan=lifespan
)


app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


@app.get("/")
def home():

    return FileResponse(
        BASE_DIR / "static" / "index.html"
    )


@app.get("/api/health")
def health():

    return {
        "status": "running",
        "ai_mode": AI_MODE
    }


def predict(patient: PatientCreate):

    try:

        return generate_health_remarks(
            patient.glucose,
            patient.haemoglobin,
            patient.cholesterol
        )

    except AIServiceError as exc:

        raise HTTPException(
            status_code=503,
            detail=str(exc)
        ) from exc


@app.post(
    "/api/patients",
    response_model=PatientResponse,
    status_code=201
)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db)
):

    existing = crud.get_patient_by_email(
        db,
        patient.email
    )

    if existing:

        raise HTTPException(
            status_code=409,
            detail="Email already exists."
        )

    remarks = predict(patient)

    try:

        return crud.create_patient(
            db, patient, remarks
        )

    except IntegrityError:

        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Duplicate or conflicting record."
        )


@app.get(
    "/api/patients",
    response_model=list[PatientResponse]
)
def read_patients(
    db: Session = Depends(get_db)
):

    return crud.get_patients(db)


@app.get(
    "/api/patients/{patient_id}",
    response_model=PatientResponse
)
def read_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):

    patient = crud.get_patient(
        db, patient_id
    )

    if not patient:

        raise HTTPException(
            status_code=404,
            detail="Patient not found."
        )

    return patient


@app.put(
    "/api/patients/{patient_id}",
    response_model=PatientResponse
)
def update_patient(
    patient_id: int,
    patient: PatientCreate,
    db: Session = Depends(get_db)
):

    record = crud.get_patient(
        db, patient_id
    )

    if not record:

        raise HTTPException(
            status_code=404,
            detail="Patient not found."
        )

    existing = crud.get_patient_by_email(
        db,
        patient.email
    )

    if existing and existing.id != patient_id:

        raise HTTPException(
            status_code=409,
            detail="Email already exists."
        )

    blood_values_changed = (
        record.glucose != patient.glucose
        or record.haemoglobin != patient.haemoglobin
        or record.cholesterol != patient.cholesterol
    )

    if blood_values_changed:

        remarks = predict(patient)

    else:

        remarks = record.remarks

    try:

        return crud.update_patient(
            db,
            record,
            patient,
            remarks
        )

    except IntegrityError:

        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Duplicate or conflicting record."
        )


@app.delete("/api/patients/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):

    record = crud.get_patient(
        db, patient_id
    )

    if not record:

        raise HTTPException(
            status_code=404,
            detail="Patient not found."
        )

    crud.delete_patient(db, record)

    return {
        "message": "Patient deleted successfully."
    }