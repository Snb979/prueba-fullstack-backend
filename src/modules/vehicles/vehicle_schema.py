from pydantic import BaseModel, Field
from typing import Optional


class VehicleCreate(BaseModel):

    brand: str = Field(
        min_length=2,
        max_length=50
    )

    model: str = Field(
        min_length=1,
        max_length=50
    )

    location: str = Field(
        min_length=2,
        max_length=100
    )

    applicant: str = Field(
        min_length=2,
        max_length=100
    )

    status: str = Field(
        min_length=2,
        max_length=50
    )


class VehicleResponse(BaseModel):

    id: int
    brand: str
    model: str
    location: str
    applicant: str
    status: str

    class Config:
        from_attributes = True