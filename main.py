from contextlib import asynccontextmanager

from azure.cosmos import CosmosClient
from fastapi import Depends, FastAPI, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.database import Base, engine, get_cosmos_client, get_db
from src.repository import DatabaseRepository
from src.utils import is_cloud


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize application resources and create database tables."""
    if not is_cloud():
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")

@app.get("/")
def get_root(request: Request):
    """Renders a simple HTML page with the current counter value."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/counter")
def read_counter(db: Session = Depends(get_db), cosmos: CosmosClient = Depends(get_cosmos_client)):  # noqa: B008
    """Return the current counter value, creating it if missing."""
    repo = DatabaseRepository()
    count = repo.get_count_db(db, cosmos)
    return {"value": count}


@app.post("/counter/increment")
def increment_counter(db: Session = Depends(get_db), cosmos: CosmosClient = Depends(get_cosmos_client)):  # noqa: B008
    """Increment the counter value and return the updated value."""
    repo = DatabaseRepository()
    count = repo.increment_counter_db(db, cosmos)
    return {"value": count}


if __name__ == "__main__":
    print("This module is not meant to be run directly. Check the README.md file " \
    "for instructions on how to start the application.")
