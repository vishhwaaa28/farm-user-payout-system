from fastapi import FastAPI
from app.core.config import settings
from app.models.user import User
from app.models.brand import Brand
from app.models.sale import Sale
from app.core.database import Base, engine
from app.models.user import User
from app.models.brand import Brand
from app.models.sale import Sale
from app.models.payout import Payout
from app.models.withdrawal import Withdrawal
from app.models.payment_transaction import PaymentTransaction

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="User Payout Management System",
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Faym User Payout Management System"
    }