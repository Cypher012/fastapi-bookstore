from sqlmodel import SQLModel, Field,Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from datetime import date, datetime
import uuid
from typing import Optional
from app.auth import models

class Book(SQLModel, table=True):
    __tablename__ = "books"
    id: uuid.UUID = Field(
        sa_column= Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id") 
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional["models.User"] = Relationship(back_populates="books")


def __repr__(self):
    return f"{self.title} - {self.author}"