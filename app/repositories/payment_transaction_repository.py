from typing import Optional

from app.enums import TransactionStatus
from app.models.payment_transaction import PaymentTransaction
from app.repositories.base_repository import BaseRepository


class PaymentTransactionRepository(BaseRepository):
    """Repository for PaymentTransaction operations."""

    def create(
        self,
        transaction: PaymentTransaction,
    ) -> PaymentTransaction:
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def get_by_withdrawal(
        self,
        withdrawal_id: int,
    ) -> Optional[PaymentTransaction]:
        return (
            self.db.query(PaymentTransaction)
            .filter(
                PaymentTransaction.withdrawal_id == withdrawal_id
            )
            .first()
        )

    def update_status(
        self,
        transaction: PaymentTransaction,
        status: TransactionStatus,
    ) -> PaymentTransaction:
        transaction.status = status

        self.db.commit()
        self.db.refresh(transaction)

        return transaction