from fastapi import APIRouter, Depends

from app.api.deps import get_withdrawal_service
from app.schemas.withdrawal import BalanceResponse
from app.services.withdrawal_service import WithdrawalService

from app.schemas.withdrawal import (
    WithdrawalRequest,
    WithdrawalResponse,
)

router = APIRouter(
    prefix="/users",
    tags=["Withdrawals"],
)


@router.get(
    "/{user_id}/balance",
    response_model=BalanceResponse,
    summary="Get available balance",
)
def get_balance(
    user_id: int,
    service: WithdrawalService = Depends(
        get_withdrawal_service
    ),
):
    balance = service.calculate_available_balance(
        user_id
    )

    return BalanceResponse(
        user_id=user_id,
        available_balance=balance,
    )
@router.post(
    "/{user_id}/withdraw",
    response_model=WithdrawalResponse,
)
def withdraw(
    user_id: int,
    request: WithdrawalRequest,
    service: WithdrawalService = Depends(
        get_withdrawal_service,
    ),
):
    result = service.withdraw(
        user_id=user_id,
        amount=request.amount,
    )

    return WithdrawalResponse(**result)