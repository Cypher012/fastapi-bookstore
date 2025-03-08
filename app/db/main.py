from sqlmodel import text, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from app.books.models import Book
from app.auth.models import User
from app.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

# Create Async Engine
# Use create_async_engine for async operations
engine = create_async_engine(
    Config.DATABASE_URL,
    echo=True,
    future=True
)

async def init_db():
    print(Config.DATABASE_URL)
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
            print("Connected to database")
    except Exception as e:
        print(f"Failed to connect: {e}")

async def get_session():
    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with Session() as session:
        yield session
