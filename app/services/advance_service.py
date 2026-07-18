from decimal import Decimal

from app.core.constants import ADVANCE_PERCENTAGE
from app.enums import PayoutStatus, PayoutType
from app.models.payout import Payout
from app.models.sale import Sale
from app.repositories.payout_repository import PayoutRepository
from app.repositories.sale_repository import SaleRepository


class AdvancePayoutService:
    """
    Service responsible for processing advance payouts.

    Business Rules:
    - Every pending sale receives an advance payout of 10%.
    - Only one advance payout can exist per sale.
    - Duplicate requests are treated as idempotent and do not create
      additional payouts.
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
        Calculate the advance payout amount.

        The advance payout is 10% of the sale earning.
        """

        return (
            earning * self.ADVANCE_PERCENTAGE
        ).quantize(Decimal("0.01"))

    def process_sale(
        self,
        sale: Sale,
    ) -> Payout | None:
        """
        Process the advance payout for a single sale.

        Returns:
            Payout:
                If a new advance payout is successfully created.

            None:
                If an advance payout already exists for the sale.
                This makes the operation idempotent and prevents
                duplicate payouts.
        """

        # Prevent duplicate advance payouts
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
            "processed": <number of payouts created>,
            "skipped": <number of sales already processed>
        }
        """

        processed = 0
        skipped = 0

        pending_sales = self.sale_repo.get_pending_sales()

        for sale in pending_sales:
            payout = self.process_sale(sale)

            if payout is not None:
                processed += 1
            else:
                skipped += 1

        return {
            "processed": processed,
            "skipped": skipped,
        }