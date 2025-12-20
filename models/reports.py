from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.base import Base


class Report(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True, autoincrement=True)
    request_id = Column(
        Integer,
        ForeignKey('requests.id', ondelete="CASCADE"),
        nullable=False,
        unique=True
    )
    text = Column(String(2048), nullable=False)
    address = Column(String(512), nullable=False)
    status = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=True)
    date_end = Column(DateTime, default=datetime.now)


    request = relationship("Request", back_populates="report", lazy="selectin")
