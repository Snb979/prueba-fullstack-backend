from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.config.database import Base


class Vehicle(Base):

    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)

    brand = Column(String(100))
    model = Column(String(100))
    location = Column(String(100))
    applicant = Column(String(100))
    status = Column(String(50))

    owner_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    owner = relationship(
        "User",
        back_populates="vehicles"
    )