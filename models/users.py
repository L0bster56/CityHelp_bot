from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from models.base import Base

from datetime import datetime

class User(Base):
    # Название таб
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    full_name = Column(String(320), nullable=False)
    language = Column(String(2), default='ru')
    phone = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    role = Column(String(215), nullable=False, default='user')

    requests = relationship("Request", back_populates="user", lazy="selectin")
