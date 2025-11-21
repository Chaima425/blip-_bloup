from sqlalchemy import Column, Integer, String, DateTime
from .database import Base

class Ping(Base):
    __tablename__ = "pings"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String)
    created_at = Column(DateTime)
