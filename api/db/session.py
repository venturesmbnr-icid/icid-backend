# app/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from api.core.config import settings

def create_engine(url: str = None):
    return create_async_engine(url or settings.DATABASE_URL, echo=False, pool_pre_ping=True)

def create_session_factory(engine):
    return async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

# The real engine is created lazily once FastAPI starts.
engine = create_engine()
AsyncSessionLocal = create_session_factory(engine)

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
