from datetime import date

import pytest

from pydantic import ValidationError
from app.schemas import PatientCreate


def valid_data():

    return {
        "full_name": "Validation Test",
        "date_of_birth": "28.01.1960",
        "email": "test@example.com",
        "glucose": 232,
        "haemoglobin": 13.5,
        "cholesterol": 180
    }


def test_valid_patient():

    patient = PatientCreate(**valid_data())

    assert patient.date_of_birth == date(
        1960, 1, 28
    )


def test_invalid_email():

    data = valid_data()

    data["email"] = "hunter@gmail"

    with pytest.raises(ValidationError):

        PatientCreate(**data)


def test_invalid_date():

    data = valid_data()

    data["date_of_birth"] = "31.11.2001"

    with pytest.raises(ValidationError):

        PatientCreate(**data)


def test_future_date():

    data = valid_data()

    data["date_of_birth"] = "01.01.2999"

    with pytest.raises(ValidationError):

        PatientCreate(**data)


def test_invalid_glucose():

    data = valid_data()

    data["glucose"] = "abc"

    with pytest.raises(ValidationError):

        PatientCreate(**data)


def test_negative_haemoglobin():

    data = valid_data()

    data["haemoglobin"] = -5

    with pytest.raises(ValidationError):

        PatientCreate(**data)