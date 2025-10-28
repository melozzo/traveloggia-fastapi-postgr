from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MemberBase(BaseModel):
    email: str
    password: str
    firstname: Optional[str] = None
    lastname: Optional[str] = None

class MemberResponse(MemberBase):
    memberid: int
    model_config = {"from_attributes": True}

class MemberRequest(BaseModel):
    email: str
    password: str
    class Config:
        extra = "ignore"

class LoginRequest(BaseModel):
    email: str
    password: str