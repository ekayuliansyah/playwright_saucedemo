from __future__ import annotations
from typing import List, Dict
from pydantic import BaseModel

class ReqresLoginSuccess(BaseModel):
    token: str

class ReqresLoginError(BaseModel):
    error: str

class ReqresUser(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: str

class ReqresListUsers(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: List[ReqresUser]
    support: Dict[str, object]

class ReqresCreateUser(BaseModel):
    name: str
    job: str
    id: str
    createdAt: str
