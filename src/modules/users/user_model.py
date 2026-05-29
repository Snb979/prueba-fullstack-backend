from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from sqlalchemy.orm import relationship

from src.config.database import Base



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), nullable=False)

    email = Column(String(150), unique=True, nullable=False)

    password = Column(String(255), nullable=False)

    role = Column(String(20), nullable=False, default="VIEWER")

    created_at = Column(DateTime, default=datetime.utcnow)
    
    vehicles = relationship(
    "Vehicle",
    back_populates="owner"
)
