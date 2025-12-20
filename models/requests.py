from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import relationship

from models.base import Base


class Request(Base):
    __tablename__ = 'requests'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger,ForeignKey('users.id', ondelete="CASCADE"),nullable=False)
    category_id = Column(Integer,ForeignKey('categories.id', ondelete="CASCADE"),nullable=False)
    text = Column(String(1024), nullable=False)
    address = Column(String(512), nullable=False)
    status = Column(String(255), nullable=False, default='new')
    created_at = Column(DateTime, default=datetime.now)



    user = relationship("User", back_populates="requests", lazy="selectin")
    category = relationship("Category", back_populates="requests", lazy="selectin")


    report = relationship(
        "Report",
        back_populates="request",
        uselist=False, lazy="selectin"
    )
