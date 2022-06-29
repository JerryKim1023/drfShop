
from email import message
from rest_framework.permissions import BasePermission
from datetime import timedelta
from django.utils import timezone
from rest_framework.exceptions import APIException
from rest_framework import status

class GenericAPIException(APIException):
    def __init__(self, status_code=None, detail=None, code=None):
        self.status_code=status_code
        super().__init__(detail=detail, code=code)


class RegistedMoreThanAWeekUser(BasePermission):
    """
    가입일 기준 1주일 이상 지난 사용자만 접근 가능
    """
    message = '가입 후 1주일 이상 지난 사용자만 사용하실 수 있습니다.'
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.join_date < (timezone.now() - timedelta(days=7)))

class IsRegisterdMoreThanThreeDaysOrReadOrReadOnly(BasePermission):
    """
    가입 후 3일 이상 지난 사용자는 쓰기, 수정, 삭제 가능 / 의외는 조회만 가능
    """
    SAFE_METHODS = ('GET', )
    message = '접근 권한이 없습니다.'
    
    def has_permission(self, request, view):
        user = request.user

        if request.method in self.SAFE_METHODS or \
            user.is_authenticated and request.user.join_date < (timezone.now() - timedelta(days=3)):
                                                              #  현재 날짜    -     3일의 값
            return True

        return False

class IsAdminOrIsAuthenticatedReadOnly(BasePermission):
    """
    admin 사용자는 모두 가능, 로그인 사용자는 조회만 가능
    """
    SAFE_METHODS = ('GET', )
    message = '접근 권한이 없습니다.'

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            response ={
                    "detail": "서비스를 이용하기 위해 로그인 해주세요.",
                }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)

        if user.is_authenticated and user.is_admin:
            return True
            
        elif user.is_authenticated and request.method in self.SAFE_METHODS:
            return True
        
        return False

class UserSeller(BasePermission):
    """
    판매자는 모두 가능
    """
    message = '접근 권한이 없습니다.'
    def has_permission(self, request, view):
        if request.user.is_seller == False:
            response ={
                    "detail": "판매자가 아닙니다. 판매자로 재로그인 해주십시오.",
                }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)
        return True
            