import secrets
import random
import string

def get_otp_code():
    return ''.join(random.choice(string.digits) for _ in range(6))

def get_session_code():
    return secrets.token_hex(6)
