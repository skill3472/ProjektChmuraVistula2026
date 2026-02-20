from src.database import Base
from sqlalchemy import Column, Integer

class Counter(Base):
    __tablename__ = "counter"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer, default=0, nullable=False)