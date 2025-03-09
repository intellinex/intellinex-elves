from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: str
    username: str
    email: Optional[str] = None
    mobile: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None