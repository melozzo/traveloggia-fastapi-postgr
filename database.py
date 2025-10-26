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
    db_url = DATABASE_URL
    try:
        # Try psycopg (v3) first
        import psycopg  # type: ignore
        if db_url.startswith("postgresql://") and "+psycopg" not in db_url:
            db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)
        engine = create_engine(db_url, echo=False, future=True)
    except Exception:
        try:
            # Fallback to psycopg2 if psycopg3/libpq not available
            import psycopg2  # type: ignore
            if db_url.startswith("postgresql://") and "+psycopg2" not in db_url:
                db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
            engine = create_engine(db_url, echo=False, future=True)
        except Exception:
            raise ImportError("Neither psycopg (v3) nor psycopg2 is available for PostgreSQL connections. Please install one of them.")
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