from typing import Optional

from app.enums import SaleStatus
from app.models.sale import Sale
from app.repositories.base_repository import BaseRepository


class SaleRepository(BaseRepository):
    """Repository for Sale database operations."""

    def create(self, sale: Sale) -> Sale:
        """
        Create a new sale.
        """
        self.db.add(sale)
        self.db.commit()
        self.db.refresh(sale)
        return sale

    def get_by_id(self, sale_id: int) -> Optional[Sale]:
        """
        Fetch a sale by its ID.
        """
        return (
            self.db.query(Sale)
            .filter(Sale.id == sale_id)
            .first()
        )

    def get_pending_sales(self) -> list[Sale]:
        """
        Return all pending sales.
        """
        return (
            self.db.query(Sale)
            .filter(Sale.status == SaleStatus.PENDING)
            .order_by(Sale.created_at)
            .all()
        )

    def update_status(
        self,
        sale: Sale,
        status: SaleStatus,
    ) -> Sale:
        """
        Update the status of a sale.
        """
        sale.status = status
        self.db.add(sale)
        self.db.commit()
        self.db.refresh(sale)
        return sale

    def get_user_sales(self, user_id: int) -> list[Sale]:
        """
        Fetch all sales for a user.
        """
        return (
            self.db.query(Sale)
            .filter(Sale.user_id == user_id)
            .order_by(Sale.created_at)
            .all()
        )