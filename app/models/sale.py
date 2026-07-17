from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums import SaleStatus
from app.models.base_model import BaseModel


class Sale(BaseModel):
    __tablename__ = "sales"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    brand_id: Mapped[int] = mapped_column(
        ForeignKey("brands.id"),
        nullable=False,
    )

    earning: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    status: Mapped[SaleStatus] = mapped_column(
        Enum(SaleStatus),
        default=SaleStatus.PENDING,
        nullable=False,
        index=True,
    )

    reconciled_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    user = relationship(
        "User",
        back_populates="sales"
    )

    brand = relationship(
        "Brand",
        back_populates="sales"
    )

    payouts = relationship(
        "Payout",
        back_populates="sale"
    )