from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)

from contextlib import asynccontextmanager

from src.config.database.db_config import settings_db


class DataBaseHepler:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(url=url, echo=echo)

        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    def get_scope_session(self):
        return async_scoped_session(
            session_factory=self.session_factory, scopefunc=current_task
        )

    async def get_db_session(self) -> AsyncSession:
        from sqlalchemy import exc

        session = self.session_factory()
        try:
            yield session
        except exc.SQLAlchemyError as error:
            await session.rollback()
            raise
        finally:
            await session.close()


db_helper = DataBaseHepler(settings_db.database_url, settings_db.DB_ECHO_LOG)
