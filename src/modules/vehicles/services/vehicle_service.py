from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.modules.vehicles.vehicle_model import Vehicle


def get_all_vehicles(db: Session):

    vehicles = db.query(Vehicle).all()

    return vehicles


def create_vehicle_service(vehicle, db: Session):

    new_vehicle = Vehicle(
        brand=vehicle.brand,
        model=vehicle.model,
        location=vehicle.location,
        applicant=vehicle.applicant,
        status=vehicle.status
    )

    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)

    return {
        "message": "Vehículo creado",
        "data": new_vehicle
    }


def get_vehicle_by_id(id: int, db: Session):

    vehicle = db.query(Vehicle).filter(Vehicle.id == id).first()

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehículo no encontrado"
        )

    return vehicle


def update_vehicle_service(id: int, vehicle, db: Session):

    vehicle_db = db.query(Vehicle).filter(Vehicle.id == id).first()

    if not vehicle_db:
        raise HTTPException(
            status_code=404,
            detail="Vehículo no encontrado"
        )

    vehicle_db.brand = vehicle.brand
    vehicle_db.model = vehicle.model
    vehicle_db.location = vehicle.location
    vehicle_db.applicant = vehicle.applicant
    vehicle_db.status = vehicle.status

    db.commit()
    db.refresh(vehicle_db)

    return {
        "message": "Vehículo actualizado",
        "data": vehicle_db
    }


def delete_vehicle_service(id: int, db: Session):

    vehicle = db.query(Vehicle).filter(Vehicle.id == id).first()

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehículo no encontrado"
        )

    db.delete(vehicle)
    db.commit()

    return {
        "message": "Vehículo eliminado"
    }