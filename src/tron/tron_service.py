from src.tron.tron_repository import WalletRepository
from src.tron.tron_schemas import WalletCreateInternal, WalletCreate
from tronpy.async_tron import AsyncTron
from tronpy.providers.async_http import AsyncHTTPProvider
from dotenv import load_dotenv


load_dotenv()


class WalletService:
    def __init__(self, repo: WalletRepository, api_key: str) -> None:
        self.repo = repo
        self.provider = AsyncHTTPProvider(api_key=api_key)
        self.tron = AsyncTron(provider=self.provider)

    async def save_wallet(self, payload: WalletCreate):
        print("CREATION")
        addres = payload.address

        balance_trx = await self.tron.get_account_balance(addres)
        resoursers = await self.tron.get_account_resource(addres)
        bandwith = await self.tron.get_bandwidth(addres)

        internal_data = WalletCreateInternal(
            address=addres,
            balance_trx=balance_trx,
            bandwith=bandwith,
            energy=resoursers.get("EnergyLimit", 0),
        )

        return await self.repo.create_wallet(internal_data)
