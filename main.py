from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from src.database import get_db, Base, engine
from src.models import Counter


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

@app.get("/counter")
def read_counter(db: Session = Depends(get_db)):
    counter = db.query(Counter).first()
    if not counter:
        counter = Counter(value=0)
        db.add(counter)
        db.commit()
        db.refresh(counter)
    return {"value": counter.value}

@app.post("/counter/increment")
def increment_counter(db: Session = Depends(get_db)):
    counter = db.query(Counter).first()
    if not counter:
        counter = Counter(value=0)
        db.add(counter)
    counter.value += 1
    db.commit()
    db.refresh(counter)
    return {"value": counter.value}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)