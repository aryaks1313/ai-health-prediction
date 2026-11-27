from datetime import date, datetime

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    ConfigDict
)


class PatientCreate(BaseModel):

    full_name: str = Field(
        min_length=2,
        max_length=150
    )

    date_of_birth: date

    email: EmailStr

    glucose: float = Field(
        gt=0,
        allow_inf_nan=False
    )

    haemoglobin: float = Field(
        gt=0,
        allow_inf_nan=False
    )

    cholesterol: float = Field(
        gt=0,
        allow_inf_nan=False
    )

    @field_validator("full_name", mode="before")
    @classmethod
    def validate_name(cls, value):

        if isinstance(value, str):
            return value.strip()

        return value

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value):
        return value.lower()

    @field_validator(
        "date_of_birth",
        mode="before"
    )
    @classmethod
    def validate_dob(cls, value):

        if isinstance(value, date):
            parsed_date = value

        else:
            parsed_date = None

            for fmt in (
                "%d/%m/%Y",
                "%d.%m.%Y",
                "%Y-%m-%d"
            ):
                try:
                    parsed_date = datetime.strptime(
                        value, fmt
                    ).date()

                    break

                except (ValueError, TypeError):
                    continue

            if parsed_date is None:
                raise ValueError(
                    "Invalid date. Use DD/MM/YYYY."
                )

        if parsed_date > date.today():
            raise ValueError(
                "Date of birth cannot be a future date."
            )

        return parsed_date


class PatientResponse(PatientCreate):

    id: int
    remarks: str

    model_config = ConfigDict(
        from_attributes=True
    )