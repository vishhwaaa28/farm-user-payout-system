from fastapi import APIRouter, Depends

from app.api.deps import get_reconciliation_service
from app.schemas.reconciliation import (
    ReconciliationRequest,
    ReconciliationResponse,
)
from app.services.reconciliation_service import ReconciliationService

router = APIRouter(
    prefix="/sales",
    tags=["Sales"],
)


@router.post(
    "/{sale_id}/reconcile",
    response_model=ReconciliationResponse,
)
def reconcile_sale(
    sale_id: int,
    request: ReconciliationRequest,
    service: ReconciliationService = Depends(
        get_reconciliation_service,
    ),
):
    result = service.reconcile_sale(
        sale_id=sale_id,
        approved=request.approved,
    )

    return ReconciliationResponse(**result)