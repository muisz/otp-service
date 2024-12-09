import environ
from fastapi import FastAPI, Depends, status, Response
from typing import Annotated, Any

from .dependencies import get_database_connection
from .schema import OTPRequest, OTPCreated, OTPCheck, OTPStatus, Error
from .model import OTP
from .repository import DbRepository
from .service import OTPService

ENV = environ.Env()
environ.Env.read_env('.env')

app = FastAPI()

@app.post('/send', response_model=OTPCreated, status_code=status.HTTP_201_CREATED)
def send(db: Annotated[Any, Depends(get_database_connection)], otp: OTPRequest):
    repository = DbRepository(db)
    service = OTPService(repository)
    created_otp = service.create_otp(otp)
    return OTPCreated(session_code=created_otp.session_code)

@app.post('/check', response_model=OTPStatus, status_code=status.HTTP_200_OK)
def check(db: Annotated[Any, Depends(get_database_connection)], otp: OTPCheck):
    repository = DbRepository(db)
    service = OTPService(repository)
    checked_otp = service.get_otp(otp.code, otp.session_code)
    valid = True
    if not service.is_valid(checked_otp):
        valid = False
    return OTPStatus(valid=valid)

@app.post('/invalidate', status_code=status.HTTP_200_OK)
def invalidate(db: Annotated[Any, Depends(get_database_connection)], otp: OTPCheck, response: Response):
    repository = DbRepository(db)
    service = OTPService(repository)
    checked_otp = service.get_otp(otp.code, otp.session_code)
    if not service.is_valid(checked_otp):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return Error(message="OTP invalid or not found")
    service.invalidate(checked_otp)
    return
