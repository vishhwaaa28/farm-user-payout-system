from decimal import Decimal
from typing import Optional

from sqlalchemy import func

from app.enums import PayoutStatus, PayoutType
from app.models.payout import Payout
from app.repositories.base_repository import BaseRepository


class PayoutRepository(BaseRepository):
    """Repository for Payout database operations."""

    def create(self, payout: Payout) -> Payout:
        """
        Create a new payout.
        """
        self.db.add(payout)
        self.db.commit()
        self.db.refresh(payout)
        return payout

    def advance_exists(self, sale_id: int) -> bool:
        """
        Check whether an advance payout already exists
        for the given sale.
        """
        return (
            self.db.query(Payout)
            .filter(
                Payout.sale_id == sale_id,
                Payout.type == PayoutType.ADVANCE,
            )
            .first()
            is not None
        )

    def get_by_sale_and_type(
        self,
        sale_id: int,
        payout_type: PayoutType,
    ) -> Optional[Payout]:
        """
        Fetch a payout for a sale by payout type.
        """
        return (
            self.db.query(Payout)
            .filter(
                Payout.sale_id == sale_id,
                Payout.type == payout_type,
            )
            .first()
        )

    def get_by_sale(self, sale_id: int) -> list[Payout]:
        """
        Fetch all payouts for a sale.
        """
        return (
            self.db.query(Payout)
            .filter(Payout.sale_id == sale_id)
            .order_by(Payout.created_at)
            .all()
        )

    def get_user_payouts(self, user_id: int) -> list[Payout]:
        """
        Fetch all payouts for a user.
        """
        return (
            self.db.query(Payout)
            .filter(Payout.user_id == user_id)
            .order_by(Payout.created_at)
            .all()
        )

    def get_total_successful_payouts(
        self,
        user_id: int,
    ) -> Decimal:
        """
        Calculate the total successful payouts
        made to a user.
        """
        total = (
            self.db.query(func.sum(Payout.amount))
            .filter(
                Payout.user_id == user_id,
                Payout.status == PayoutStatus.SUCCESS,
            )
            .scalar()
        )

        return total or Decimal("0.00")