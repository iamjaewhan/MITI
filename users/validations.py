import re
        
class UserPasswordValidator:
    REGEX_PASSWORD = '^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,}$'
    default_error_messege = '유효한 비밀번호가 아닙니다.'
    
    def check_password(value):
        if not re.fullmatch(UserPasswordValidator.REGEX_PASSWORD, value):
            raise ValueError(UserPasswordValidator.default_error_messege)