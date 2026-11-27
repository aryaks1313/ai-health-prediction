from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models import Patient
from app.schemas import PatientCreate


def get_patients(db: Session):

    return db.scalars(
        select(Patient).order_by(Patient.id)
    ).all()


def get_patient(db: Session, patient_id: int):

    return db.get(Patient, patient_id)


def get_patient_by_email(
    db: Session,
    email: str
):

    return db.scalar(
        select(Patient).where(
            Patient.email == email
        )
    )


def create_patient(
    db: Session,
    patient: PatientCreate,
    remarks: str
):

    record = Patient(
        **patient.model_dump(),
        remarks=remarks
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


def update_patient(
    db: Session,
    record: Patient,
    patient: PatientCreate,
    remarks: str
):

    for key, value in patient.model_dump().items():

        setattr(record, key, value)

    record.remarks = remarks

    db.commit()
    db.refresh(record)

    return record


def delete_patient(
    db: Session,
    record: Patient
):

    db.delete(record)
    db.commit()