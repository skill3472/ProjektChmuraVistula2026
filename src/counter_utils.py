from sqlalchemy.orm import Session

from src.models import Counter


def create_counter(db: Session) -> Counter:
    """Create a new counter with value 0 and persist it."""
    counter = Counter(value=0)
    db.add(counter)
    db.commit()
    db.refresh(counter)
    return counter
