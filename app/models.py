from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    Text,
    DateTime,
    func
)

from app.database import Base


class Patient(Base):

    __tablename__ = "patients"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    full_name = Column(
        String(150),
        nullable=False
    )

    date_of_birth = Column(
        Date,
        nullable=False
    )

    email = Column(
        String(254),
        unique=True,
        index=True,
        nullable=False
    )

    glucose = Column(Float, nullable=False)

    haemoglobin = Column(Float, nullable=False)

    cholesterol = Column(Float, nullable=False)

    remarks = Column(Text, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )