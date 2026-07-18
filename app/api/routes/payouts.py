from fastapi import APIRouter, Depends

from app.api.deps import get_advance_service
from app.schemas.payout import AdvancePayoutResponse
from app.services.advance_service import AdvancePayoutService

router = APIRouter(
    prefix="/payouts",
    tags=["Payouts"],
)


@router.post(
    "/advance",
    response_model=AdvancePayoutResponse,
    summary="Generate advance payouts",
)
def generate_advance_payouts(
    service: AdvancePayoutService = Depends(get_advance_service),
) -> AdvancePayoutResponse:
    """
    Generate advance payouts for all pending sales.
    """

    result = service.run()

    return AdvancePayoutResponse(
        processed=result["processed"],
        skipped=result["skipped"],
    )