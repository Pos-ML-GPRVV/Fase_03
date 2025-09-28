from sqlalchemy import Column, Integer, DateTime, Float,func
from app.database import Base

class ErrorMetrics(Base):
    __tablename__ = "error_metrics"

    #columns
    id = Column(Integer, primary_key=True, index=True)
    mse = Column(Float(8,2), nullable=False)
    rmse = Column(Float(8,2), nullable=False)
    mape = Column(Float(8,2), nullable=False)
    created_at = Column(DateTime, default=func.now())

    