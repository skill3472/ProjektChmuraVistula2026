import os

from azure.cosmos import CosmosClient
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.utils import is_cloud

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Provide a database session for request handling."""
    if is_cloud():
        return None
    else:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()


def get_cosmos_client():
    """Create and return a Cosmos DB client if in cloud environment."""
    if "WEBSITE_SITE_NAME" in os.environ:
        url = os.environ.get("COSMOS_URL")
        key = os.environ.get("COSMOS_KEY")
        return CosmosClient(url, credential=key)
    return None
