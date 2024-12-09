from pydantic import BaseModel
from typing import Union

class OTP(BaseModel):
    id: Union[int, None] = None
    code: str
    destination: str
    session_code: str
    is_active: bool
