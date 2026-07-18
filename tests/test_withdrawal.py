from decimal import Decimal

import app.models

from app.core.database import Base, SessionLocal, engine
from app.models.brand import Brand
from app.models.user import User
from app.models.sale import Sale

from app.repositories.sale_repository import SaleRepository
from app.repositories.payout_repository import PayoutRepository
from app.repositories.withdrawal_repository import WithdrawalRepository
from app.repositories.payment_transaction_repository import (
    PaymentTransactionRepository,
)

from app.services.advance_service import AdvancePayoutService
from app.services.reconciliation_service import ReconciliationService
from app.services.withdrawal_service import WithdrawalService


def seed_data(db):
    """Insert sample user, brand and sale."""

    user = User(
        name="Alice",
        email="alice@example.com",
    )

    brand = Brand(
        name="Nike",
    )

    db.add_all([user, brand])
    db.commit()

    db.refresh(user)
    db.refresh(brand)

    sale = Sale(
        user_id=user.id,
        brand_id=brand.id,
        earning=Decimal("1000.00"),
    )

    db.add(sale)
    db.commit()
    db.refresh(sale)

    return user, sale


def main():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    user, sale = seed_data(db)

    sale_repo = SaleRepository(db)
    payout_repo = PayoutRepository(db)
    withdrawal_repo = WithdrawalRepository(db)
    payment_repo = PaymentTransactionRepository(db)

    # Step 1: Advance payout
    advance_service = AdvancePayoutService(
        sale_repo,
        payout_repo,
    )

    advance_service.run()

    # Step 2: Approve sale
    reconciliation_service = ReconciliationService(
        sale_repo,
        payout_repo,
    )

    reconciliation_service.reconcile_sale(
        sale.id,
        approved=True,
    )

    # Step 3: Withdrawal service
    withdrawal_service = WithdrawalService(
        payout_repo,
        withdrawal_repo,
        payment_repo,
    )

    print("\n========== BALANCE ==========")

    balance = withdrawal_service.calculate_available_balance(
        user.id
    )

    print(balance)

    print("\n========== WITHDRAW ==========")

    result = withdrawal_service.withdraw(
        user.id,
        Decimal("400.00"),
    )

    print(result)

    print("\n========== REMAINING BALANCE ==========")

    balance = withdrawal_service.calculate_available_balance(
        user.id
    )

    print(balance)

    print("\n========== WITHDRAWALS ==========")

    withdrawals = withdrawal_repo.get_user_withdrawals(user.id)

    for withdrawal in withdrawals:
        print(
            f"Withdrawal={withdrawal.id} | "
            f"Amount={withdrawal.amount} | "
            f"Status={withdrawal.status.value}"
        )

    print("\n========== TRANSACTIONS ==========")

    for withdrawal in withdrawals:
        txn = payment_repo.get_by_withdrawal(
            withdrawal.id
        )

        print(
            f"Txn={txn.id} | "
            f"Gateway={txn.gateway_reference} | "
            f"Status={txn.status.value}"
        )

    print("\n========== INSUFFICIENT BALANCE TEST ==========")

    try:
        withdrawal_service.withdraw(
            user.id,
            Decimal("700.00"),
        )
    except ValueError as e:
        print(e)

    db.close()


if __name__ == "__main__":
    main()