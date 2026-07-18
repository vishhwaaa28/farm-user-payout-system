from decimal import Decimal
import app.models
from app.core.database import SessionLocal
from app.enums import SaleStatus
from app.repositories.payout_repository import PayoutRepository
from app.repositories.sale_repository import SaleRepository
from app.services.advance_service import AdvancePayoutService
from app.models.user import User
from app.models.brand import Brand
from app.models.sale import Sale
from app.models.payout import Payout
from app.models.withdrawal import Withdrawal
from app.models.payment_transaction import PaymentTransaction

def seed_data(db):
    """Insert sample data if the database is empty."""

    if db.query(User).first():
        print("Database already contains data. Skipping seed.")
        return

    user = User(
        name="John Doe",
        email="john@example.com"
    )

    brand = Brand(
        name="Nike"
    )

    db.add(user)
    db.add(brand)
    db.commit()

    db.refresh(user)
    db.refresh(brand)

    sales = [
        Sale(
            user_id=user.id,
            brand_id=brand.id,
            earning=Decimal("1000.00"),
            status=SaleStatus.PENDING,
        ),
        Sale(
            user_id=user.id,
            brand_id=brand.id,
            earning=Decimal("2500.00"),
            status=SaleStatus.PENDING,
        ),
        Sale(
            user_id=user.id,
            brand_id=brand.id,
            earning=Decimal("500.00"),
            status=SaleStatus.PENDING,
        ),
    ]

    db.add_all(sales)
    db.commit()

    print("Sample data inserted successfully.")


def main():
    db = SessionLocal()

    try:
        seed_data(db)

        sale_repo = SaleRepository(db)
        payout_repo = PayoutRepository(db)

        service = AdvancePayoutService(
            sale_repo,
            payout_repo,
        )

        print("\n========== FIRST RUN ==========")

        result = service.run()

        print(result)

        print("\n========== SECOND RUN ==========")

        result = service.run()

        print(result)

        print("\n========== PAYOUTS ==========")

        payouts = payout_repo.get_user_payouts(1)

        for payout in payouts:
            print(
                f"Sale: {payout.sale_id}, "
                f"Type: {payout.type.value}, "
                f"Amount: {payout.amount}"
            )

    finally:
        db.close()


if __name__ == "__main__":
    main()