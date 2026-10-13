from core import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

AsyncSessionLocal = sessionmaker(bind=engine, 
                                class_=AsyncSession, 
                                expire_on_commit=False, 
                                autoflush=False)

Base = declarative_base()