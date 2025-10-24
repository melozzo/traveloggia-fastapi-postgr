import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Prefer DATABASE_URL from environment (Heroku sets this for you)
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Heroku provides a DATABASE_URL in the form postgresql://user:pass@host:port/dbname
    # SQLAlchemy will try to import a DBAPI based on the URL. If the environment
    # has the new psycopg (v3) package installed (importable as `psycopg`), prefer
    # the `postgresql+psycopg://` scheme so SQLAlchemy uses that driver instead
    # of trying to import psycopg2.
    
    db_url = DATABASE_URL
    try:
        # prefer psycopg (v3) when available
        import psycopg  # type: ignore
        if db_url.startswith("postgresql://") and "+psycopg" not in db_url:
            db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)
    except Exception:
        # psycopg not available; try psycopg2 (if installed) by making no change
        pass
    engine = create_engine(db_url, echo=False, future=True)
else:
    # Fallback for local development - use SQLite file
    local_sqlite = "sqlite:///./dev.db"
    engine = create_engine(local_sqlite, connect_args={"check_same_thread": False}, echo=True, future=True)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()