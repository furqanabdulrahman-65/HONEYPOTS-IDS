from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AttackLogBase(BaseModel):
    ip_address: str
    method: str
    path: str
    headers: str
    query_params: str
    body: Optional[str] = None
    user_agent: Optional[str] = None

class AttackLogCreate(AttackLogBase):
    pass

class AttackLogResponse(AttackLogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
