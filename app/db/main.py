from sqlmodel import text, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from app.books.models import Book
from app.auth.models import User
from app.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
import ssl

# Create an SSL context for asyncpg
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False  # Optional, based on your SSL requirements
ssl_ctx.verify_mode = ssl.CERT_NONE  # Change this if you need proper verification

# Create Async Engine with SSL support
engine = create_async_engine(
    Config.DATABASE_URL, 
    echo=True, 
    future=True,
    connect_args={"ssl": ssl_ctx}  # Fix: Use "ssl" instead of "sslmode"
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
