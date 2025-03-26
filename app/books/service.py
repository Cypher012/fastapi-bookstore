from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel, BookUpdateModel
from sqlmodel import select, desc
from .models import Book
from datetime import datetime

class BookService:
    async def get_all_books(self, session: AsyncSession):
        stmt = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(stmt)
        return result.all()
    
    async def get_user_books(self,book_id: str ,session: AsyncSession):
        stmt = select(Book).where(Book.user_id == book_id).order_by(desc(Book.created_at))
        result = await session.exec(stmt)
        return result.all()
    
    async def get_book(self, book_uid: str, session: AsyncSession):
        stmt = select(Book).where(Book.id == book_uid)  
        result = await session.exec(stmt)
        return result.first()
    
    async def create_book(self,book_data: BookCreateModel, user_id: str ,session: AsyncSession):
        new_book = Book(**book_data.model_dump())  
        new_book.published_date = datetime.strptime(book_data.published_date, "%Y-%m-%d")

        new_book.user_id = user_id
        
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book
    
    async def update_book(self, book_uid: str, update_data: BookUpdateModel, session: AsyncSession):
        book_to_update = await self.get_book(book_uid, session)
        if book_to_update:
            update_data_dict = update_data.model_dump(exclude_unset=True)
            for key, value in update_data_dict.items():
                setattr(book_to_update, key, value)
            await session.commit()
            await session.refresh(book_to_update) 
            return book_to_update
        return None
        
    async def delete_book(self, book_uid: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)
        if book_to_delete:
            await session.delete(book_to_delete) 
            await session.commit()
            return book_to_delete
        return None
