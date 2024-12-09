from typing import Union

from .repository import OTPRepository
from .model import OTP
from .schema import OTPRequest
from .exception import ServiceError

class OTPService:
    def __init__(self, repository: OTPRepository):
        self.repository = repository
    
    def create_otp(self, otp: OTPRequest) -> OTP:
        return self.repository.create(otp)
    
    def get_otp(self, code: str, session_code: str) -> Union[OTP, None]:
        otp = self.repository.get_otp(code, session_code)
        return otp

    def invalidate(self, otp: OTP):
        otp.is_active = False
        self.repository.update(otp)

    def is_valid(self, otp: Union[OTP, None]):
        if otp is None or not otp.is_active:
            return False
        return True
