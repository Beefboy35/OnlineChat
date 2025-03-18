import uuid
from datetime import datetime
from decimal import Decimal
from typing import Annotated
from sqlalchemy import func, TIMESTAMP, Integer, inspect
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
from app.config import database_url


engine = create_async_engine(url=database_url)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'

    def to_dict(self, exclude_none: bool = False):
        """
        Parses a model object into python dictionary.

        Args:
            exclude_none (bool): Whether to exclude None values from the dict

        Returns:
            dict: Dictionary with object data in it
        """
        result = {}
        for column in inspect(self.__class__).columns:
            value = getattr(self, column.key)

            # Parse special data types
            if isinstance(value, datetime):
                value = value.isoformat()
            elif isinstance(value, Decimal):
                value = float(value)
            elif isinstance(value, uuid.UUID):
                value = str(value)

            # Add value to the result
            if not exclude_none or value is not None:
                result[column.key] = value

        return result

    def __repr__(self) -> str:
        """String object view for better debugging."""
        return f"<{self.__class__.__name__}(id={self.id}, created_at={self.created_at})>"
