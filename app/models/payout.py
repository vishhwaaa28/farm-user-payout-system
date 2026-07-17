from sqlalchemy import Enum, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal
from app.enums import PayoutStatus, PayoutType
from app.models.base_model import BaseModel


class Payout(BaseModel):
    __tablename__ = "payouts"

    __table_args__ = (
        UniqueConstraint(
            "sale_id",
            "type",
            name="uq_sale_payout_type",
        ),
    )

    sale_id: Mapped[int] = mapped_column(
        ForeignKey("sales.id"),
        nullable=False,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    type: Mapped[PayoutType] = mapped_column(
        Enum(PayoutType),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    status: Mapped[PayoutStatus] = mapped_column(
        Enum(PayoutStatus),
        default=PayoutStatus.PENDING,
        nullable=False,
    )

    sale = relationship(
        "Sale",
        back_populates="payouts",
    )

    user = relationship(
        "User",
        back_populates="payouts",
    )