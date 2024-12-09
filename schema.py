from pydantic import BaseModel


class OTPRequest(BaseModel):
    destination: str

class OTPCreated(BaseModel):
    session_code: str

class OTPCheck(BaseModel):
    code: str
    session_code: str

class OTPStatus(BaseModel):
    valid: bool

class Error(BaseModel):
    message: str
