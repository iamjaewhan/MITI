from rest_framework.exceptions import APIException


class UnParticipatableException(APIException):
    status_code = 400
    default_detail = '더이상 참여할 수 없는 경기입니다.'
    default_code = 'Bad Request'
    

class DuplicatedParticipationException(APIException):
    status_code = 400
    default_detail = '이미 참여한 경기입니다.'
    default_code = 'Bad Request'
    

class FullGameException(APIException):
    status_code = 400
    default_detail = '모집이 완료된 경기입니다.'
    default_code = 'Bad Request'