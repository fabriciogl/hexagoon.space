from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    token: Optional[str]
    exp: Optional[datetime]

    class Config:
        title = 'token'