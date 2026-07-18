from decimal import Decimal
import uuid

from app.enums import (
    TransactionStatus,
    WithdrawalStatus,
)
from app.models.payment_transaction import PaymentTransaction
from app.models.withdrawal import Withdrawal
from app.repositories.payment_transaction_repository import (
    PaymentTransactionRepository,
)
from app.repositories.payout_repository import PayoutRepository
from app.repositories.withdrawal_repository import (
    WithdrawalRepository,
)


class WithdrawalService:
    """
    Handles user withdrawal requests.

    Workflow:
    1. Calculate available balance.
    2. Validate requested amount.
    3. Create withdrawal.
    4. Simulate payment gateway.
    5. Create payment transaction.
    6. Mark withdrawal completed.
    """

    def __init__(
        self,
        payout_repo: PayoutRepository,
        withdrawal_repo: WithdrawalRepository,
        payment_repo: PaymentTransactionRepository,
    ):
        self.payout_repo = payout_repo
        self.withdrawal_repo = withdrawal_repo
        self.payment_repo = payment_repo

    def calculate_available_balance(
        self,
        user_id: int,
    ) -> Decimal:
        """
        Calculate the current withdrawable balance.
        """

        total_payouts = (
            self.payout_repo.get_total_successful_payouts(
                user_id
            )
        )

        total_withdrawn = (
            self.withdrawal_repo.get_total_completed_withdrawals(
                user_id
            )
        )

        return total_payouts - total_withdrawn

    def withdraw(
        self,
        user_id: int,
        amount: Decimal,
    ) -> dict:
        """
        Process a withdrawal request.
        """

        if amount <= Decimal("0.00"):
            raise ValueError(
                "Withdrawal amount must be greater than zero."
            )

        available = self.calculate_available_balance(
            user_id
        )

        if amount > available:
            raise ValueError(
                "Insufficient balance."
            )

        # Step 1: Create withdrawal request
        withdrawal = Withdrawal(
            user_id=user_id,
            amount=amount,
            status=WithdrawalStatus.PENDING,
        )

        withdrawal = self.withdrawal_repo.create(
            withdrawal
        )

        # Step 2: Simulate payment gateway
        transaction = PaymentTransaction(
            withdrawal_id=withdrawal.id,
            gateway_reference=str(uuid.uuid4()),
            status=TransactionStatus.SUCCESS,
            response="Payment processed successfully.",
        )

        transaction = self.payment_repo.create(
            transaction
        )

        # Step 3: Mark withdrawal completed
        withdrawal = self.withdrawal_repo.complete(
            withdrawal
        )

        return {
            "withdrawal_id": withdrawal.id,
            "transaction_id": transaction.id,
            "amount": withdrawal.amount,
            "status": withdrawal.status.value,
            "available_balance": self.calculate_available_balance(
                user_id
            ),
        }