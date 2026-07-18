from fastapi import FastAPI

from app.api.router import api_router
from app.core.exception_handlers import (
    register_exception_handlers,
)

app = FastAPI(
    title="Faym User Payout Management System",
    version="1.0.0",
)

register_exception_handlers(app)

app.include_router(api_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to the Faym User Payout Management API"
    }