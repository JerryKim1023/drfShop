# Create your views here.
# views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.db.models import F
from rest_framework.exceptions import APIException

from rest_framework import permissions

# 회원가입 API
from rest_framework_simplejwt.tokens import RefreshToken

from user.serializers import UserSerializer

# 회원가입
class SignupAPI(APIView):
    def post(self, request):
        '''
        사용자 정보를 입력받아 create 하는 함수
        '''
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid(): 
            user_serializer.save() # 정상
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        # is_valid 함수에서 raise_exeption=True를 주면 아래처럼 코드 간소화 가능
        # user_serializer.is_valid(raise_exception=True)
        # user_serializer.save() # 정상
        # return Response(user_serializer.data, status=status.HTTP_200_OK)
      

# 로그인
class LoginAPI(APIView):
    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 맞지 않습니다."},
                            status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)

        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)
        return Response({
                            "message": 'login success',
                            'refresh': refresh_token,
                            'access': access_token
                        }, status=status.HTTP_200_OK)


class LogoutAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    template_name = 'index.html'
    # 로그아웃
    def get(self, request):
        auth.logout(request)
        return Response({"message": "로그아웃 성공!!"}, status=status.HTTP_200_OK)

        

    # # 수정
    # def put(self, request, obj_id):
        
    #     user_update = UserModel.objects.get(id=obj_id)
    #     # 오브젝트, data , partial 넘기기
    #     user_serializer = UserSerializer(user_update, data=request.data, partial=True)
    #     user_serializer.is_valid(raise_exception=True)
    #     user_serializer.save() # 정상
    #     return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        
    #     # is_valid 함수에서 raise_exeption=True를 주면 위처럼 코드 간소화 가능
    #     # if user_serializer.is_valid(): 
    #     #     user_serializer.save() # 정상
    #     #     return Response(user_serializer.data, status=status.HTTP_200_OK)

    #     # return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # # 삭제
    # def delete(self, request, obj_id):
        
    #     try:
    #         user_delete = UserModel.objects.get(obj_id)  
    #     except UserModel.DoesNotExist:
    #      # some event						   status=400
    #         return Response({"message": "오브젝트가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
    #     user_delete.delete()
    #     # 오브젝트, data , partial 넘기기
    #     return Response({"message": f"{UserModel.username} 정보가 더 이상 존재하지 않습니다."}, status=status.HTTP_200_OK)
