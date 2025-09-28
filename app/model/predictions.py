from sqlalchemy import Column, Integer, String, DateTime, Float,func, UniqueConstraint
from app.database import Base

class Predictions(Base):
    __tablename__ = "predictions"

    #columns
    id = Column(Integer, primary_key=True, index=True)
    month = Column(String(100), nullable=False)
    value = Column(Float(8,2), nullable=False)
    created_at = Column(DateTime, default=func.now())

    __table_args__ = (
        UniqueConstraint('month', name='uix_month_key'), 
    )