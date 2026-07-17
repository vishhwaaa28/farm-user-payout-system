from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


class Brand(BaseModel):
    __tablename__ = "brands"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    sales = relationship(
        "Sale",
        back_populates="brand"
    )