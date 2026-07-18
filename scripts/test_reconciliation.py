from decimal import Decimal

from app.core.database import Base, SessionLocal, engine

import app.models

from app.enums import PayoutType
from app.models.brand import Brand
from app.models.user import User
from app.models.sale import Sale
from app.repositories.sale_repository import SaleRepository
from app.repositories.payout_repository import PayoutRepository
from app.services.advance_service import AdvancePayoutService
from app.services.reconciliation_service import ReconciliationService


def seed_data(db):
    """Insert sample data."""

    user = User(
        name="Alice Jane",
        email="alice@example.com",
    )
    brand = Brand(name="Nike")

    db.add_all([user, brand])
    db.commit()

    db.refresh(user)
    db.refresh(brand)

    approved_sale = Sale(
        user_id=user.id,
        brand_id=brand.id,
        earning=Decimal("1000.00"),
    )

    rejected_sale = Sale(
        user_id=user.id,
        brand_id=brand.id,
        earning=Decimal("500.00"),
    )

    db.add_all([approved_sale, rejected_sale])
    db.commit()

    db.refresh(approved_sale)
    db.refresh(rejected_sale)

    return approved_sale, rejected_sale


def main():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    approved_sale, rejected_sale = seed_data(db)

    sale_repo = SaleRepository(db)
    payout_repo = PayoutRepository(db)

    # Create advance payouts
    advance_service = AdvancePayoutService(
        sale_repo,
        payout_repo,
    )

    advance_service.run()

    reconciliation_service = ReconciliationService(
        sale_repo,
        payout_repo,
    )

    print("\n========== APPROVED ==========")

    result = reconciliation_service.reconcile_sale(
        approved_sale.id,
        approved=True,
    )

    print(result)

    print("\n========== REJECTED ==========")

    result = reconciliation_service.reconcile_sale(
        rejected_sale.id,
        approved=False,
    )

    print(result)

    print("\n========== PAYOUTS ==========")

    payouts = payout_repo.get_user_payouts(approved_sale.user_id)

    for payout in payouts:
        print(
            f"Sale={payout.sale_id} | "
            f"Type={payout.type.value} | "
            f"Amount={payout.amount}"
        )

    db.close()


if __name__ == "__main__":
    main()