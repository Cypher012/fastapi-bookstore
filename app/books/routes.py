from fastapi import APIRouter, Depends, HTTPException, status
from app.books.models import Book
from app.db.main import get_session
from app.books.service import BookService
from app.books.schemas import BookCreateModel, BookUpdateModel  
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Annotated
from app.auth.dependencies import AccessTokenBearer, RoleChecker



book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin", "user"]))



async def get_auth_providers(
    session: Annotated[AsyncSession, Depends(get_session)],
    token_details: Annotated[str, Depends(access_token_bearer)],
):
    return {"session": session, "token_details": token_details}


@book_router.get("/", response_model=List[Book], status_code=status.HTTP_200_OK, dependencies=[role_checker])
async def get_books(auth_providers: dict = Depends(get_auth_providers)):
    session = auth_providers["session"]
    print(auth_providers["token_details"])
    return await book_service.get_all_books(session)



@book_router.get("/user/{user_id}", response_model=List[Book], status_code=status.HTTP_200_OK, dependencies=[role_checker])
async def get_user_books(user_id: str, auth_providers: dict = Depends(get_auth_providers)):
    session = auth_providers["session"]
    print(auth_providers["token_details"])
    return await book_service.get_user_books(user_id, session)



@book_router.get("/{book_uid}", response_model=Book, status_code=status.HTTP_200_OK, dependencies=[role_checker])
async def get_book(book_uid: str, auth_providers: dict = Depends(get_auth_providers)):
    session = auth_providers["session"]
    book = await book_service.get_book(book_uid, session)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book



@book_router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED, dependencies=[role_checker])
async def create_book(book_data: BookCreateModel,auth_providers: dict = Depends(get_auth_providers)):
    session = auth_providers["session"]
    print("auth_providers['token_details'] : ", auth_providers["token_details"])
    user_id = (auth_providers["token_details"]).get("user")["user_id"]
    return await book_service.create_book(book_data,user_id ,session)

@book_router.put("/{book_uid}", response_model=BookUpdateModel, status_code=status.HTTP_200_OK, dependencies=[role_checker])
async def update_book(book_uid: str, update_data: BookUpdateModel, auth_providers: dict = Depends(get_auth_providers)):
    session = auth_providers["session"]
    updated_book = await book_service.update_book(book_uid, update_data, session)
    if updated_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book 

@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_book(book_uid: str, auth_providers: dict = Depends(get_auth_providers)):
    session = auth_providers["session"]
    deleted_book = await book_service.delete_book(book_uid, session)
    if deleted_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return None
