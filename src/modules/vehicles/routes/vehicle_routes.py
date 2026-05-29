from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.config.dependencies import get_db

from src.modules.vehicles.vehicle_schema import (
    VehicleCreate
)

from src.modules.auth.auth_bearer import JWTBearer
from src.modules.auth.role_verifier import RoleChecker
from src.modules.auth.current_user import get_current_user

from src.modules.vehicles.controllers.vehicle_controller import (
    get_vehicles_controller,
    create_vehicle_controller,
    get_vehicle_controller,
    update_vehicle_controller,
    delete_vehicle_controller
)

router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"]
)


@router.get("/", dependencies=[Depends(JWTBearer())])
def get_vehicles(
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    return get_vehicles_controller(
        db,
        current_user,
        skip,
        limit,
        status
    )

@router.post(
    "/",
    dependencies=[
        Depends(JWTBearer()),
        Depends(RoleChecker(["admin"]))
    ]
)
def create_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    return create_vehicle_controller(
        vehicle,
        db,
        current_user
    )

@router.get(
    "/{id}",
    dependencies=[Depends(JWTBearer())]
)
def get_vehicle(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    return get_vehicle_controller(
        id,
        db,
        current_user
    )

@router.put(
    "/{id}",
    dependencies=[
        Depends(JWTBearer()),
        Depends(RoleChecker(["admin"]))
    ]
)
def update_vehicle(
    id: int,
    vehicle: VehicleCreate,
    db: Session = Depends(get_db)
):

    return update_vehicle_controller(
        id,
        vehicle,
        db
    )


@router.delete(
    "/{id}",
    dependencies=[
        Depends(JWTBearer()),
        Depends(RoleChecker(["admin"]))
    ]
)
def delete_vehicle(
    id: int,
    db: Session = Depends(get_db)
):

    return delete_vehicle_controller(
        id,
        db
    )