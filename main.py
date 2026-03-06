from azure.cosmos import CosmosClient
from fastapi import Depends, FastAPI, Request
from fastapi.templating import Jinja2Templates

from src.database import get_cosmos_client
from src.repository import DatabaseRepository

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def get_root(request: Request):
    """Renders a simple HTML page with the current counter value."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/counter")
def read_counter(cosmos: CosmosClient = Depends(get_cosmos_client)):  # noqa: B008
    """Return the current counter value, creating it if missing."""
    repo = DatabaseRepository()
    count = repo.get_count_db(None, cosmos)
    return {"value": count}

@app.post("/counter/increment")
def increment_counter(cosmos: CosmosClient = Depends(get_cosmos_client)):  # noqa: B008
    """Increment the counter value and return the updated value."""
    repo = DatabaseRepository()
    count = repo.increment_counter_db(None, cosmos)
    return {"value": count}
