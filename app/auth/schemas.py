from pydantic import BaseModel, Field
from typing import Annotated
from uuid import UUID
from datetime import datetime
from typing import List
from app.books.schemas import Book

class UserResponseModel(BaseModel):
    id: UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    

class UserBooksModel(UserResponseModel):
    books: List[Book]

class UserCreateModel(BaseModel):
    first_name: Annotated[str, Field(max_length=25)]
    last_name: Annotated[str, Field(max_length=25)]
    username: str = Field(max_length= 10)
    email: str = Field(max_length = 40)
    password: str = Field(min_length = 6)

class UserLogin(BaseModel):
    email: str
    password: str = Field(min_length = 6)