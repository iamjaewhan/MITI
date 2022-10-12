from django.core.exceptions import ValidationError
from django.utils import timezone

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
        
        
class BaseTokenValidator:
    message = '유효한 토큰 포맷이 아닙니다.'
    code = 'invalid'
    token_regex = '^[a-zA-Z0-9]+\.[a-zA-Z0-9]+\.[a-zA-Z0-9\-\_]+$'
    
    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
            
    def __call__(self, value):
        if not value:
            raise ValidationError(self.message, code=self.code, params={'value': value})
        
        if not re.fullmatch(self.token_regex, value):
            raise ValidationError(self.message, code=self.code, params={'value': value})
        
    def __eq__(self, other):
        return (
            isinstance(other, BaseTokenValidator)
            and (self.message == other.message)
            and (self.code == other.code)
        )


class GameTimeValidator:
    """_summary_
    경기 시작시간, 종료시간 유효성 검사

    Raises:
        ValidationError: 현재시간보다 앞선 시점일 경우 ValidationError
    """
    
    message = '유효한 경기 시간이 아닙니다.'
    code = 'invalid'
    
    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
            
    def __call__(self, value):
        if not value:
            raise ValidationError(self. message, code=self.code, params={'value': value})
        
        if not value > timezone.now():
            raise ValidationError(self. message, code=self.code, params={'value': value})
