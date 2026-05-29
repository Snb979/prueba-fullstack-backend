from sqlalchemy.orm import Session

from src.modules.vehicles.services.vehicle_service import (
    update_vehicle_service,
    delete_vehicle_service
)

from fastapi import HTTPException
from src.modules.vehicles.vehicle_model import Vehicle


def get_vehicles_controller(
    db,
    current_user,
    skip,
    limit,
    status
):

    query = db.query(Vehicle)

    if current_user["role"] != "admin":
        query = query.filter(
            Vehicle.owner_id == current_user["id"]
        )

    if status:
        query = query.filter(
            Vehicle.status == status
        )

    return query.offset(skip).limit(limit).all()


def create_vehicle_controller(
    vehicle,
    db,
    current_user
):

    new_vehicle = Vehicle(
        brand=vehicle.brand,
        model=vehicle.model,
        location=vehicle.location,
        applicant=vehicle.applicant,
        status=vehicle.status,
        owner_id=current_user["id"]
    )

    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)

    return {
        "message": "Vehículo creado",
        "data": new_vehicle
    }


def get_vehicle_controller(
    id,
    db,
    current_user
):

    vehicle = db.query(Vehicle).filter(
        Vehicle.id == id
    ).first()

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehículo no encontrado"
        )

    if (
        current_user["role"] != "admin"
        and vehicle.owner_id != current_user["id"]
    ):
        raise HTTPException(
            status_code=403,
            detail="No autorizado"
        )

    return vehicle


def update_vehicle_controller(id: int, vehicle, db: Session):

    return update_vehicle_service(id, vehicle, db)


def delete_vehicle_controller(id: int, db: Session):

    return delete_vehicle_service(id, db)