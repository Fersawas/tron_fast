from src.schemas.base_schema import Base


class WalletCreate(Base):
    address: str


class WalletCreateInternal(Base):
    address: str
    balance_trx: float
    bandwith: int
    energy: int


class WalletRetrieve(Base):
    id: int
    address: str
    balance_trx: float
    bandwith: int
    energy: int

    class Config:
        orm_mode = True
