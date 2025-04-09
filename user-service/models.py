from sqlalchemy import Column, Integer, String, Boolean
from .database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    name = Column(String(255))
    bio = Column(String(500), nullable=True)
    avatar_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
