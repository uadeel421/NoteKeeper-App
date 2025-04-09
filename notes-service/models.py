from sqlalchemy import Column, Integer, String
from database import Base


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(255), nullable=False)
    owner_id = Column(Integer, nullable=False, index=True)
