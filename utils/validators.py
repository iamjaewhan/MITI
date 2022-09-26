from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

import re
        

class PasswordValidator:
    message = '비밀번호는 8자 이상의 영문 대소문자와 숫자, 특수문자를 포함하여야 합니다.'
    code = 'invalid'
    password_regex = '^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,}$'
    
    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
            
    def __call__(self, value):
        if not value:
            raise ValidationError(self.message, code=self.code, params={'value': value})
        
        if not re.fullmatch(self.password_regex, value):
            raise ValidationError(self.message, code=self.code, params={'value': value})

    def __eq__(self, other):
        return (
            isinstance(other, PasswordValidator)
            and (self.message == other.message)
            and (self.code == other.code)
        )