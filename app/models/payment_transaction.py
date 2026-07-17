from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums import TransactionStatus
from app.models.base_model import BaseModel


class PaymentTransaction(BaseModel):
    __tablename__ = "payment_transactions"

    withdrawal_id: Mapped[int] = mapped_column(
        ForeignKey("withdrawals.id"),
        nullable=False,
        unique=True,
    )

    gateway_reference: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    status: Mapped[TransactionStatus] = mapped_column(
        Enum(TransactionStatus),
        nullable=False,
    )

    response: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    withdrawal = relationship(
        "Withdrawal",
        back_populates="transaction",
    )