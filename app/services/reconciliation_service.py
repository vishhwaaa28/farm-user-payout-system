from app.enums import PayoutType, SaleStatus
from app.repositories.payout_repository import PayoutRepository
from app.repositories.sale_repository import SaleRepository


class ReconciliationService:
    """
    Handles reconciliation of pending sales.

    Business Rules:
    - APPROVED:
        * Pay remaining amount (earning - advance)
        * Mark sale as APPROVED
    - REJECTED:
        * Reverse advance using an adjustment payout
        * Mark sale as REJECTED
    """

    def __init__(
        self,
        sale_repo: SaleRepository,
        payout_repo: PayoutRepository,
    ):
        self.sale_repo = sale_repo
        self.payout_repo = payout_repo

    def reconcile_sale(
        self,
        sale_id: int,
        approved: bool,
    ) -> dict:
        """
        Reconcile a pending sale.

        Args:
            sale_id: ID of the sale.
            approved: True if approved, False if rejected.

        Returns:
            Dictionary containing reconciliation result.
        """

        # Fetch sale
        sale = self.sale_repo.get_by_id(sale_id)

        if sale is None:
            raise ValueError("Sale not found.")

        # Prevent duplicate reconciliation
        if sale.status != SaleStatus.PENDING:
            raise ValueError("Sale has already been reconciled.")

        # Fetch advance payout
        advance = self.payout_repo.get_by_sale_and_type(
            sale.id,
            PayoutType.ADVANCE,
        )

        if advance is None:
            raise ValueError("Advance payout not found.")

        if approved:
            # Pay remaining amount
            remaining = sale.earning - advance.amount

            self.payout_repo.create_payout(
                sale_id=sale.id,
                user_id=sale.user_id,
                payout_type=PayoutType.FINAL,
                amount=remaining,
            )

            self.sale_repo.reconcile(
                sale,
                SaleStatus.APPROVED,
            )

            action = "FINAL_PAYOUT"

        else:
            # Reverse advance
            self.payout_repo.create_payout(
                sale_id=sale.id,
                user_id=sale.user_id,
                payout_type=PayoutType.ADJUSTMENT,
                amount=-advance.amount,
            )

            self.sale_repo.reconcile(
                sale,
                SaleStatus.REJECTED,
            )

            action = "ADJUSTMENT"

        return {
            "sale_id": sale.id,
            "status": sale.status.value,
            "action": action,
        }