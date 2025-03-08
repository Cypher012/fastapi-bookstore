from fastapi import FastAPI
from app.books.routes import book_router
from app.auth.routes import auth_router
from contextlib import asynccontextmanager
from app.db.main import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("Server is starting.....")
        await init_db()
        yield
    except:
        print("Server is shutting down.....")


version = "v1"

app = FastAPI(
    title="Book API",                               
    description="A simple book API",
    version=version,
    lifespan= lifespan
)


app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])


