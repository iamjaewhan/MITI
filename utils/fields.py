from rest_framework.fields import CharField

from utils.validators import PasswordValidator


class PasswordField(CharField):
    default_error_messages = {
        'invalid' : '유효한 비밀번호가 아닙니다.'
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        validator = PasswordValidator()
        self.validators.append(validator)