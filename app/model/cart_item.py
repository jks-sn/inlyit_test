from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base

class CartItem(Base):
    __tablename__ = 'cart_items'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)

    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")
