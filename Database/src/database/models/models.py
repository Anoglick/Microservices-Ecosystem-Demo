import uuid

from sqlalchemy import JSON, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    def __repr__(self):
        fields = [
            f"{column.name}={repr(getattr(self, column.name))}"
            for column in self.__table__.columns
        ]

        return f'<{self.__class__.__name__}> {", ".join(fields)}'

class Microservices(Base):
    __tablename__ = 'microservices'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True
    )
    name: Mapped[str] = mapped_column(String, unique=True)
    tag: Mapped[str]
    route: Mapped[str]
    method: Mapped[str]
    microservice_url: Mapped[str]
    schema_name: Mapped[str]
    microservice_schema: Mapped[dict] = mapped_column(JSON)
    test_data: Mapped[list[dict]] = mapped_column(JSON)
    active: Mapped[bool] = mapped_column(default=True)


