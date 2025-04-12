import os
from typing import List
from src.config.database.db_helper import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from src.tron.tron_schemas import WalletCreate, WalletCreateInternal, WalletRetrieve
from src.tron.tron_repository import WalletRepository
from src.tron.tron_service import WalletService

from starlette.status import HTTP_400_BAD_REQUEST

from fastapi import Depends, APIRouter, HTTPException

from dotenv import load_dotenv


router = APIRouter(prefix="/tron", tags=["tron"])


load_dotenv()


@router.post("/wallets/")
async def create_wallet(
    payload: WalletCreate,
    db_session: AsyncSession = Depends(db_helper.get_db_session),
) -> WalletCreateInternal:
    try:
        repo = WalletRepository(session=db_session)
        service = WalletService(repo=repo, api_key=os.environ.get("API_KEY"))
        return await service.save_wallet(payload)
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))


@router.get("/wallets/", response_model=List[WalletRetrieve])
async def get_wallets(
    limit: int = 10,
    offset: int = 0,
    db_session: AsyncSession = Depends(db_helper.get_db_session),
) -> WalletRetrieve:
    try:
        repo = WalletRepository(session=db_session)
        wallet = await repo.get_wallets(limit=limit, offset=offset)
        if not wallet:
            raise HTTPException(HTTP_400_BAD_REQUEST, "Wallet not found")
        return wallet
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))
