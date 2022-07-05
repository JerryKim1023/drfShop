from django.shortcuts import get_object_or_404, render
from rest_framework.renderers import TemplateHTMLRenderer

from django.contrib import auth
# Create your views here.
# views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from rest_framework.exceptions import APIException
# from drfShop.permissions import UserSeller

from user.models import User as UserModel
# from user.models import UserSeller as UserSellerModel


from django.contrib.auth import authenticate, login
from django.db.models import F

from datetime import datetime, timedelta, timezone

from user.serializers import UserSignupSerializer, UserSerializer
# from user.serializers import UserSellerSerializer

class UserSignupView(APIView):
    
    #모든 사용자에 대해서 user 정보와 userpofile 정보를 가져오고
    # 같은 취미를 가진 사람들을 출력하기
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        # user = request.user
        user = UserModel.objects.all().order_by('?').first()
        # user = UserModel.objects.get(id=12)
        # serializer에 queryset을 인자로 줄 경우 many=True 옵션을 사용해야 한다.
        serialized_user_data = UserSerializer(user).data # 오브젝트를 넣어서 직렬화해주기
        print(serialized_user_data)
        return Response(serialized_user_data, status=status.HTTP_200_OK)

        # return data
        """
        {
            "username": "user",
            "password": "pbkdf2_sha256$320000$u5YnmKo9luab9csqWpzRsa$pKfqHnBiF5Rgdo1Mj9nxNOdhpAl9AhPVXFPXkbPz7Mg=",
            "fullname": "user's name",
            "email": "user@email.com"
        }
        """

    # 회원가입
    def post(self, request):
        '''
        사용자 정보를 입력받아 create 하는 함수
        '''
        user_serializer = UserSignupSerializer(data=request.data)
        print('1')
        print(user_serializer)
        if user_serializer.is_valid(): 
            print('2')
            user_serializer.save() # 정상
            print('3')
            print(user_serializer.data)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        print('4')
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        # is_valid 함수에서 raise_exeption=True를 주면 아래처럼 코드 간소화 가능
        # user_serializer.is_valid(raise_exception=True)
        # user_serializer.save() # 정상
        # return Response(user_serializer.data, status=status.HTTP_200_OK)
      
    # 수정
    def put(self, request, obj_id):
        
        user_update = UserModel.objects.get(id=obj_id)
        # 오브젝트, data , partial 넘기기
        user_serializer = UserSerializer(user_update, data=request.data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save() # 정상
        return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        
        # is_valid 함수에서 raise_exeption=True를 주면 위처럼 코드 간소화 가능
        # if user_serializer.is_valid(): 
        #     user_serializer.save() # 정상
        #     return Response(user_serializer.data, status=status.HTTP_200_OK)

        # return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 삭제
    def delete(self, request, obj_id):
        
        try:
            user_delete = UserModel.objects.get(obj_id)  
        except UserModel.DoesNotExist:
         # some event						   status=400
            return Response({"message": "오브젝트가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        user_delete.delete()
        # 오브젝트, data , partial 넘기기
        return Response({"message": f"{UserModel.username} 정보가 더 이상 존재하지 않습니다."}, status=status.HTTP_200_OK)


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    # 로그인
    def post(self, request):
        print(request.data)
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        print('3333311')
        user = auth.authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            print('11111')
            auth.login(request, user)
            print('222222222')
            return Response({"result": "success"}, status=status.HTTP_200_OK)

        return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'
    # 로그아웃
    def get(self, request):
        auth.logout(request)
        return Response({"message": "로그아웃 성공!!"}, status=status.HTTP_200_OK)

# class UserSellerApiView(APIView):
    
#     #모든 사용자에 대해서 user 정보와 userpofile 정보를 가져오고
#     # 같은 취미를 가진 사람들을 출력하기
#     permission_classes = [UserSeller]
#     def get(self, request):
#         # user = request.user
#         user = UserSellerModel.objects.all().order_by('?').first()
#         # serializer에 queryset을 인자로 줄 경우 many=True 옵션을 사용해야 한다.
#         serialized_user_data = UserSerializer(user).data # 오브젝트를 넣어서 직렬화해주기
#         return Response(serialized_user_data, status=status.HTTP_200_OK)

#         # return data
#         """
#         {
#             "username": "user",
#             "password": "pbkdf2_sha256$320000$u5YnmKo9luab9csqWpzRsa$pKfqHnBiF5Rgdo1Mj9nxNOdhpAl9AhPVXFPXkbPz7Mg=",
#             "fullname": "user's name",
#             "email": "user@email.com"
#         }
#         """

#     # 회원가입
#     def post(self, request):
#         '''
#         사용자 정보를 입력받아 create 하는 함수
#         '''
#         user_serializer = UserSellerSerializer(data=request.data)
#         user_serializer.is_valid(raise_exception=True)
#         user_serializer.save() # 정상
#         return Response(user_serializer.data, status=status.HTTP_200_OK)
        
#         # is_valid 함수에서 raise_exeption=True를 주면 위처럼 코드 간소화 가능
#         # if user_serializer.is_valid(): 
#         #     user_serializer.save() # 정상
#         #     return Response(user_serializer.data, status=status.HTTP_200_OK)

#         # return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
#     # 수정
#     def put(self, request, obj_id):
        
#         user_update = UserSellerModel.objects.get(id=obj_id)
#         # 오브젝트, data , partial 넘기기
#         user_serializer = UserSellerSerializer(user_update, data=request.data, partial=True)
#         user_serializer.is_valid(raise_exception=True)
#         user_serializer.save() # 정상
#         return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        
#         # is_valid 함수에서 raise_exeption=True를 주면 위처럼 코드 간소화 가능
#         # if user_serializer.is_valid(): 
#         #     user_serializer.save() # 정상
#         #     return Response(user_serializer.data, status=status.HTTP_200_OK)

#         # return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # 삭제
#     def delete(self, request, obj_id):
        
#         try:
#             user_delete = UserSellerModel.objects.get(obj_id)  
#         except UserSellerModel.DoesNotExist:
#          # some event						   status=400
#             return Response({"message": "오브젝트가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
#         user_delete.delete()
#         # 오브젝트, data , partial 넘기기
#         return Response({"message": f"{UserSellerModel.username} 정보가 더 이상 존재하지 않습니다."}, status=status.HTTP_200_OK)
