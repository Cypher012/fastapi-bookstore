from sqlmodel import Relationship, SQLModel, Field,Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime
from app.books import models
class User(SQLModel, table = True):
    __tablename__ = "users"
    id: uuid.UUID = Field(
        sa_column= Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    username: str
    email: str
    password_hash: str = Field(exclude=True)
    first_name: str
    last_name: str
    role: str = Field(sa_column = Column(pg.VARCHAR(255),nullable = False ,server_default="user", default = "user"))
    is_verified: bool = False
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    books: list["models.Book"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})


    def __repr__(self):
        return f"<User {self.username}>"

"""
class User:
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool = false
    created_at: datetime
    updated_at: datetime
"""