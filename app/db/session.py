from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# 1. The engine: knows how to physically connect to PostgreSQL
engine = create_engine(settings.database_url)

# 2. The session factory: produces new Session objects when called
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# 3. The FastAPI dependency: one fresh session per HTTP request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()