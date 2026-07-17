from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    sales = relationship(
        "Sale",
        back_populates="user"
    )

    payouts = relationship(
        "Payout",
        back_populates="user"
    )

    withdrawals = relationship(
        "Withdrawal",
        back_populates="user"
    )