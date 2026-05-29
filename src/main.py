from fastapi import FastAPI

from src.config.database import engine, Base

from src.modules.users.user_model import User
from src.modules.vehicles.vehicle_model import Vehicle

from src.modules.users.routes.user_routes import router as user_router

from src.modules.vehicles.routes.vehicle_routes import router as vehicle_router


from fastapi.exceptions import RequestValidationError

from src.exceptions.handlers import (
    validation_exception_handler,
    generic_exception_handler
)

from src.middlewares.requestLogger import (
    RequestLoggerMiddleware
)

app = FastAPI()
app.add_middleware(
    RequestLoggerMiddleware
)
app.include_router(vehicle_router)
app.include_router(user_router)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    Exception,
    generic_exception_handler
)



@app.get("/")
def root():
    return {
        "message": "Backend running successfully"
    }