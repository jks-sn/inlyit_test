from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    cart_items = relationship("CartItem", back_populates="user")
