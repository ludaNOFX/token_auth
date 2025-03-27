from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    # AsyncSession,
    # async_sessionmaker
)


def _create_engine(url: str, echo: bool = False) -> AsyncEngine:
    return create_async_engine(
        url=url,
        future=True,
        echo=echo,
        pool_pre_ping=False,
        pool_size=20,
        max_overflow=10,
        pool_recycle=1200,
        pool_timeout=6000,
    )


# class SessionFactory()
