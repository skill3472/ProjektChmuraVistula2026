from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.counter_utils import create_counter
from src.database import Base, engine, get_db
from src.models import Counter


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize application resources and create database tables."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")

@app.get("/")
def get_root(request: Request):
    """Renders a simple HTML page with the current counter value."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/counter")
def read_counter(db: Session = Depends(get_db)):  # noqa: B008
    """Return the current counter value, creating it if missing."""
    counter = db.query(Counter).first()
    if not counter:
        counter = create_counter()
    return {"value": counter.value}


@app.post("/counter/increment")
def increment_counter(db: Session = Depends(get_db)):  # noqa: B008
    """Increment the counter value and return the updated value."""
    counter = db.query(Counter).first()
    if not counter:
        counter = create_counter()
    counter.value += 1
    db.commit()
    db.refresh(counter)
    return {"value": counter.value}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=80)
