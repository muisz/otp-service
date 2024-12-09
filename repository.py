from datetime import datetime
from fastapi import Depends
from typing import Annotated, Any, Union

from .schema import OTPRequest
from .model import OTP
from .dependencies import get_database_connection
from .utils import get_otp_code, get_session_code

class OTPRepository:
    def create(self, otp: OTPRequest) -> OTP:
        raise NotImplementedError()
    
    def get_otp(self, code: str, session_code: str) -> Union[OTP, None]:
        raise NotImplementedError()
    
    def update(self, otp: OTP):
        raise NotImplementedError()

class DbRepository(OTPRepository):
    def __init__(self, db):
        self.db = db
    
    def create(self, otp: OTPRequest) -> OTP:
        with self.db.cursor() as cursor:
            code = get_otp_code()
            session_code = get_session_code()
            cursor.execute("insert into otps (code, destination, session_code, is_active) values (%s, %s, %s, %s);", [code, otp.destination, session_code, True])
            self.db.commit()
            return OTP(code=code, destination=otp.destination, session_code=session_code, is_active=True)
    
    def get_otp(self, code: str, session_code: str) -> Union[OTP, None]:
        with self.db.cursor() as cursor:
            cursor.execute("select id, code, destination, session_code, is_active from otps where code = %s and session_code = %s;", [code, session_code])
            result = cursor.fetchone()
            if not result:
                return None
            return OTP(id=result[0], code=result[1], destination=result[2], session_code=result[3], is_active=result[4])
    
    def update(self, otp: OTP):
        with self.db.cursor() as cursor:
            cursor.execute(
                "update otps set code = %s, destination = %s, session_code = %s, is_active = %s, updated_at = %s where id = %s",
                [otp.code, otp.destination, otp.session_code, otp.is_active, datetime.now(), otp.id]
            )
            self.db.commit()
