from decimal import Decimal
from app.enums import PayoutStatus, PayoutType
from app.models.payout import Payout
from app.models.sale import Sale
from app.repositories.payout_repository import PayoutRepository
from app.repositories.sale_repository import SaleRepository
from app.core.constants import ADVANCE_PERCENTAGE


class AdvancePayoutService:
    """
    Service responsible for processing advance payouts.

    Business Rules:
    - Every pending sale receives an advance payout of 10%.
    - Advance payout is created only once.
    - Service is idempotent.
    """

    ADVANCE_PERCENTAGE = ADVANCE_PERCENTAGE

    def __init__(
        self,
        sale_repo: SaleRepository,
        payout_repo: PayoutRepository,
    ):
        self.sale_repo = sale_repo
        self.payout_repo = payout_repo

    def calculate_advance(
        self,
        earning: Decimal,
    ) -> Decimal:
        """
        Calculate 10% advance amount.
        """

        return (
            earning * self.ADVANCE_PERCENTAGE
        ).quantize(Decimal("0.01"))

    def process_sale(
        self,
        sale: Sale,
    ) -> Payout | None:
        """
        Process advance payout for a single sale.

        Returns:
            Payout if created.
            None if already processed.
        """

        if self.payout_repo.advance_exists(sale.id):
            return None

        advance_amount = self.calculate_advance(
            sale.earning
        )

        payout = Payout(
            sale_id=sale.id,
            user_id=sale.user_id,
            type=PayoutType.ADVANCE,
            amount=advance_amount,
            status=PayoutStatus.SUCCESS,
        )

        return self.payout_repo.create(payout)

    def run(self) -> dict:
        """
        Process advance payouts for all pending sales.

        Returns:
        {
            "processed": x,
            "skipped": y
        }
        """

        processed = 0
        skipped = 0

        pending_sales = self.sale_repo.get_pending_sales()

        for sale in pending_sales:

            payout = self.process_sale(sale)

            if payout:
                processed += 1
            else:
                skipped += 1

        return {
            "processed": processed,
            "skipped": skipped,
        }