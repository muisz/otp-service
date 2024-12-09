import unittest

from .repository import OTPRepository
from .model import OTP
from .service import OTPService
from .schema import OTPRequest


class MockOTPRepository(OTPRepository):
    otps: list[OTP] = []

    def create(self, otp: OTP) -> OTP:
        otp.id = len(self.otps) + 1
        self.otps.append(otp)
        return otp
    
    def get_otp(self, code: str, session_code: str):
        for otp in self.otps:
            if otp.code == code and otp.session_code == session_code:
                return otp
        return None
    
    def update(self, otp: OTP):
        for index in range(len(self.otps)):
            if self.otps[index].id == otp.id:
                self.otps[index] = otp
                break


class TestOTPService(unittest.TestCase):
    def setUp(self):
        self.repository = MockOTPRepository()
        self.service = OTPService(self.repository)

    def test_create_otp(self):
        otp = OTPRequest(destination='test@email.com')
        
        created_otp = self.service.create_otp(otp)
        
        self.assertIsNotNone(created_otp.code)
        self.assertIsNotNone(created_otp.session_code)
        self.assertTrue(created_otp.is_active)
    
    def test_get_otp(self):
        otp = OTPRequest(destination='test@email.com')
        created_otp = self.service.create_otp(otp)
        
        result = self.service.get_otp(created_otp.code, created_otp.session_code)

        self.assertIsNotNone(result)
    
    def test_invalidate(self):
        otp = OTPRequest(destination='test@email.com')
        created_otp = self.service.create_otp(otp)
        otp = self.service.get_otp(created_otp.code, created_otp.session_code)

        self.service.invalidate(otp)
        otp = self.service.get_otp(created_otp.code, created_otp.session_code)
        
        self.assertFalse(otp.is_active)
    
    def test_is_valid(self):
        otp = OTPRequest(destination='test@email.com')
        created_otp = self.service.create_otp(otp)

        result = self.service.is_valid(created_otp)

        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
