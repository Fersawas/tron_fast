from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.wallet_model import Wallet
from src.tron.tron_schemas import WalletCreateInternal


class WalletRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_wallet(self, wallet: WalletCreateInternal):
        existing_wallet = await self.get_wallet(wallet.address)
        if existing_wallet:
            raise ValueError("Wallet already exists")
        new_wallet = Wallet(**wallet.model_dump())
        self.session.add(new_wallet)
        try:
            await self.session.commit()
            await self.session.refresh(new_wallet)
            return new_wallet
        except Exception as e:
            await self.session.rollback()
            raise ValueError(f"Failed to create wallet: {e}")

    async def get_wallets(self, limit: int, offset: int):
        result = await self.session.execute(select(Wallet).offset(offset).limit(limit))

        return result.scalars().all()

    async def get_wallet(self, address: str):
        result = await self.session.execute(
            select(Wallet).where(Wallet.address == address)
        )

        return result.scalars().first()

    async def delete_wallet(self, address: str):
        wallet = await self.get_wallet(address)
        if wallet:
            await self.session.delete(wallet)
            await self.session.commit()
