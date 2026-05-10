from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .database import Base

class AttackLog(Base):
    __tablename__ = "attack_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    ip_address = Column(String(50), index=True)
    method = Column(String(10))
    path = Column(String(255))
    headers = Column(Text)
    query_params = Column(Text)
    body = Column(Text)
    user_agent = Column(String(255))
