from rest_framework import permissions, status
from rest_framework.exceptions import APIException
from rest_framework.permissions import BasePermission


class GenericAPIException(APIException):
    def __init__(self, status_code, detail=None, code=None):
        self.status_code = status_code
        super().__init__(detail=detail, code=code)


class IsAdminOrReadOnly(BasePermission):
    """
        관리자는 모두 가능, 로그인한 사용자는 조회만 가능
    """
    SAFE_METHODS = ('GET',)

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            response = {
                "detail": "서비스를 이용하려면 로그인 해야합니다."
            }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail=response)

        # 로그인 & 조회
        if user.is_authenticated and request.method in self.SAFE_METHODS:
            return True

        # 로그인 & 관리자 권한 -> 생성, 수정, 삭제 가능
        return user.is_authenticated and user.is_admin


class IsSellerOrReadOnly(BasePermission):
    """
        판매자는 모두 가능, 로그인한 사용자는 조회만 가능
    """
    SAFE_METHODS = ('GET',)

    def has_permission(self, request, view):
        # 조회
        if request.method in self.SAFE_METHODS:
            return True

        user = request.user
        if not user.is_authenticated:
            response = {
                "detail": "서비스를 이용하려면 로그인 해야합니다."
            }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail=response)

        # 로그인 & 관리자 권한 -> 생성, 수정, 삭제 가능
        return user.is_authenticated and user.is_seller

    def has_object_permission(self, request, view, obj):
        return obj.seller == request.user


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            response = {
                "detail": "서비스를 이용하려면 로그인 해야합니다."
            }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail=response)
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.customer == request.user  # author 필드가 있다고 가정