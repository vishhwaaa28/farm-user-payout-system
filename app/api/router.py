from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.payouts import router as payout_router
from app.api.routes.reconciliation import (
    router as reconciliation_router,
)
from app.api.routes.withdrawals import (
    router as withdrawal_router,
)

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(payout_router)
api_router.include_router(reconciliation_router)
api_router.include_router(withdrawal_router)