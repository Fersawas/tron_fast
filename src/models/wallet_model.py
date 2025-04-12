from sqlalchemy import String, Integer, Float, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal

from src.models.base_model import Base


class Wallet(Base):
    __tablename__ = "wallets"

    address: Mapped[str] = mapped_column(
        String(length=150), unique=True, nullable=False
    )
    balance_trx: Mapped[Decimal] = mapped_column(Numeric(20, 6))
    bandwith: Mapped[int] = mapped_column(Integer())
    energy: Mapped[int] = mapped_column(Integer())
