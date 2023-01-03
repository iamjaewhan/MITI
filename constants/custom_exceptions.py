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
    

class DuplicatedPaymentException(APIException):
    status_code = 400
    default_detail = '이미 결제가 완료되었습니다.'
    default_code = 'Bad Request'
    

class RequestFailException(APIException):
    status_code = 500
    default_detail = '서버 내부에 오류가 발생하였습니다.'
    default_code = 'Internal Server Error'
    

class UnchangeableStatusException(APIException):
    status_code = 400
    default_detail = '결제 상태를 변경할 수 없습니다.'
    default_code = 'Bad Request'
