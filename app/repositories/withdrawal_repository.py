from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import func

from app.enums import WithdrawalStatus
from app.models.withdrawal import Withdrawal
from app.repositories.base_repository import BaseRepository


class WithdrawalRepository(BaseRepository):
    """Repository for Withdrawal database operations."""

    def create(
        self,
        withdrawal: Withdrawal,
    ) -> Withdrawal:
        """
        Persist a new withdrawal.
        """
        self.db.add(withdrawal)
        self.db.commit()
        self.db.refresh(withdrawal)
        return withdrawal

    def get_by_id(
        self,
        withdrawal_id: int,
    ) -> Optional[Withdrawal]:
        """
        Fetch a withdrawal by its ID.
        """
        return (
            self.db.query(Withdrawal)
            .filter(Withdrawal.id == withdrawal_id)
            .first()
        )

    def get_user_withdrawals(
        self,
        user_id: int,
    ) -> list[Withdrawal]:
        """
        Fetch all withdrawals for a user.
        """
        return (
            self.db.query(Withdrawal)
            .filter(Withdrawal.user_id == user_id)
            .order_by(Withdrawal.created_at)
            .all()
        )

    def get_total_completed_withdrawals(
        self,
        user_id: int,
    ) -> Decimal:
        """
        Calculate the total amount successfully withdrawn by a user.
        """
        total = (
            self.db.query(func.sum(Withdrawal.amount))
            .filter(
                Withdrawal.user_id == user_id,
                Withdrawal.status == WithdrawalStatus.SUCCESS,
            )
            .scalar()
        )

        return total or Decimal("0.00")

    def complete(
        self,
        withdrawal: Withdrawal,
    ) -> Withdrawal:
        """
        Mark a withdrawal as successfully completed.
        """
        withdrawal.status = WithdrawalStatus.SUCCESS
        withdrawal.completed_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(withdrawal)

        return withdrawal