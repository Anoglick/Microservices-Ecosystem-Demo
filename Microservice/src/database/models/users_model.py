from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    def __repr__(self):
        fields = [
            f"{column.name}={repr(getattr(self, column.name))}"
            for column in self.__table__.columns
        ]

        return f'<{self.__class__.__name__}> {", ".join(fields)}'
    
class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    age: Mapped[int]
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    
    password = ...

    # Дописать дату создания и дату последнего входа пользователя


