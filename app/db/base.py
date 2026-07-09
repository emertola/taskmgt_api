from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models.

    Every model in app/models/ inherits from this Base.
    SQLAlchemy uses it to keep a registry of all tables
    it knows about (used later for migrations, etc.).
    """
    pass