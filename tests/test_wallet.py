import pytest
from fastapi import status
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from app import app

from src.tron.tron_schemas import WalletCreateInternal
from src.models.wallet_model import Wallet
from src.tron.tron_repository import WalletRepository
from src.config.database.db_helper import db_helper

from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_create_wallet():
    with patch("src.tron.tron_service.AsyncTron") as mock_tron_class, patch(
        "src.tron.tron_service.load_dotenv"
    ), patch.dict("os.environ", {"API_KEY": "fake_api_key"}), patch(
        "src.tron.tron_repository.WalletRepository.get_wallet", return_value=None
    ), patch(
        "src.tron.tron_repository.WalletRepository.create_wallet"
    ) as mock_create:

        mock_tron = AsyncMock()
        mock_tron_class.return_value = mock_tron
        mock_tron.get_account_balance.return_value = 100.0
        mock_tron.get_account_resource.return_value = {"EnergyLimit": 200}
        mock_tron.get_bandwidth.return_value = 500

        mock_wallet = Wallet(
            address="TVDPdZ8whQFqooSCDPwWL2yeLYrEnyEfax",
            balance_trx=100.0,
            bandwith=500,
            energy=200,
        )
        mock_create.return_value = mock_wallet

        client = TestClient(app)
        wallet_data = {"address": "TVDPdZ8whQFqooSCDPwWL2yeLYrEnyEfax"}

        response = client.post("tron/wallets", json=wallet_data)

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["address"] == wallet_data["address"]


@pytest.mark.asyncio
async def test_wallet_repository_create(
    session: AsyncSession,
):
    repo = WalletRepository(session=session)

    wallet_data = WalletCreateInternal(
        address="TNS1Xr4cpa5dRjFGSqAh8ASB5LioHf3xH1f",
        balance_trx=100.0,
        bandwith=500,
        energy=200,
    )

    created_wallet = await repo.create_wallet(wallet_data)

    assert created_wallet is not None
    assert created_wallet.address == wallet_data.address

    db_wallet = await repo.get_wallets(limit=10, offset=0)
    assert db_wallet is not None


@pytest.mark.asyncio
async def test_get_wallets(session):
    repo = WalletRepository(session=session)

    # Добавляем тестовые кошельки
    wallets = [
        Wallet(address="ADDR1", balance_trx=100.0, bandwith=500, energy=200),
        Wallet(address="ADDR2", balance_trx=50.0, bandwith=300, energy=150),
    ]
    session.add_all(wallets)
    await session.commit()

    result = await repo.get_wallets(limit=10, offset=0)

    assert len(result) == 2
    assert result[0].address == "ADDR1"
    assert result[1].address == "ADDR2"
