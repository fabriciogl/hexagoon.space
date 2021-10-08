from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class Token(BaseModel):
    token: Optional[str]
    exp: Optional[datetime]
    roles: Optional[List[str]]

    class Config:
        title = 'token'