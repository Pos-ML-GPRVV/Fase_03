from sqlalchemy import Column, Integer, String, DateTime, Float,func, UniqueConstraint
from app.database import Base

class Ipca(Base):
    __tablename__ = "ipca"

    #columns
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(255), nullable=False)
    month = Column(String(100), nullable=False)
    type = Column(String(255), nullable=False)
    value = Column(Float(8,2), nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    __table_args__ = (
        UniqueConstraint('category', 'type', 'month', name='uix_ipca_key'),
    )

    def __repr__(self) -> str:
        return f"Ipca(id={self.id!r}, category='{self.category}', month='{self.month}')"