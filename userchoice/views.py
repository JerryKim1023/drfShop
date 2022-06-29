from django.shortcuts import get_object_or_404, render
from rest_framework.renderers import TemplateHTMLRenderer

# Create your views here.
import os
from django.shortcuts import render
# views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status

from django.db.models import F

from django.views.static import serve

from datetime import datetime, timedelta, timezone
from userchoice.models import Review as ReviewModel
from product.models import Product as ProductModel
from product.models import Category as CategoryModel
from user.models import User as UserModel

from userchoice.serializers import CartSerializer, ReviewSerializer

class CartView(APIView):
    
    #모든 사용자에 대해서 user 정보와 userpofile 정보를 가져오고
    # 같은 취미를 가진 사람들을 출력하기
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'cart.html'
    def get(self, request):
        user = request.user
        # user = UserModel.objects.all().order_by('?').first()
        # user = UserModel.objects.get(id=12)
        # serializer에 queryset을 인자로 줄 경우 many=True 옵션을 사용해야 한다.
        serialized_cart_data = CartSerializer(user).data # 오브젝트를 넣어서 직렬화해주기
        return Response(serialized_cart_data, status=status.HTTP_200_OK)

        # return data
        """
        {
            "username": "user",
            "password": "pbkdf2_sha256$320000$u5YnmKo9luab9csqWpzRsa$pKfqHnBiF5Rgdo1Mj9nxNOdhpAl9AhPVXFPXkbPz7Mg=",
            "fullname": "user's name",
            "email": "user@email.com"
        }
        """

    # 장바구니 넣기
    def post(self, request):
        '''
        사용자 정보를 입력받아 create 하는 함수
        '''
        cart_serializer = CartSerializer(data=request.data)
        print('1')
        print(cart_serializer)
        if cart_serializer.is_valid(): 
            print('2')
            cart_serializer.save() # 정상
            print('3')
            print(cart_serializer.data)
            return Response(cart_serializer.data, template_name='cart.html', status=status.HTTP_200_OK)
        print('4')
        return Response(cart_serializer.errors, template_name='/', status=status.HTTP_400_BAD_REQUEST)
        
        
        # is_valid 함수에서 raise_exeption=True를 주면 아래처럼 코드 간소화 가능
        # user_serializer.is_valid(raise_exception=True)
        # user_serializer.save() # 정상
        # return Response(user_serializer.data, status=status.HTTP_200_OK)
      
    # 장바구니 수정
    def put(self, request, obj_id):
        
        user_update = UserModel.objects.get(id=obj_id)
        # 오브젝트, data , partial 넘기기
        cart_serializer = CartSerializer(user_update, data=request.data, partial=True)
        cart_serializer.is_valid(raise_exception=True)
        cart_serializer.save() # 정상
        return Response(cart_serializer.data, status=status.HTTP_200_OK)
        
        
        # is_valid 함수에서 raise_exeption=True를 주면 위처럼 코드 간소화 가능
        # if user_serializer.is_valid(): 
        #     user_serializer.save() # 정상
        #     return Response(user_serializer.data, status=status.HTTP_200_OK)

        # return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 장바구니삭제
    def delete(self, request, obj_id):
        
        try:
            user_delete = UserModel.objects.get(obj_id)  
        except UserModel.DoesNotExist:
         # some event						   status=400
            return Response({"message": "장바구니가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        cart_serializer = CartSerializer(user_delete, data=request.data, partial=True)
        cart_serializer.delete()
        # 오브젝트, data , partial 넘기기
        return Response({"message": f"{UserModel.username} 정보가 더 이상 존재하지 않습니다."}, status=status.HTTP_200_OK)




#상품별로처리
class ReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'cart.html'
    
    #상품별로 상품에 대해서 review 정보 가져오고
    permission_classes = [permissions.AllowAny]
    def get(self, request, obj_id):  # 상품 id 받아옴
        product = ProductModel.get(obj_id)
        serialized_review_data = ReviewSerializer(product).data # 오브젝트를 넣어서 직렬화해주기
        return Response(serialized_review_data, many=True, status=status.HTTP_200_OK)

        # return data
        """
        {
            "username": "user",
            "password": "pbkdf2_sha256$320000$u5YnmKo9luab9csqWpzRsa$pKfqHnBiF5Rgdo1Mj9nxNOdhpAl9AhPVXFPXkbPz7Mg=",
            "fullname": "user's name",
            "email": "user@email.com"
        }
        """

    # 상품 리뷰 등록
    def post(self, request, obj_id): # 상품 id 받아옴
        '''
        상품 정보를 입력받아 review create 하는 함수
        '''
        product = ProductModel.objects.get(obj_id)
        review_serializer = ReviewSerializer(product, data=request.data)
        if review_serializer.is_valid(): 
            review_serializer.save() # 정상
            return Response(review_serializer.data, status=status.HTTP_200_OK)

        return Response(review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
    # 상품 리뷰 수정
    def put(self, request, obj_id): # 댓글 id 받아옴
        
        product_sale_info_change = ProductModel.objects.get(id=obj_id)
        # 오브젝트, data , partial 넘기기
        review_serializer = ReviewSerializer(product_sale_info_change, data=request.data, partial=True)
        review_serializer.is_valid(raise_exception=True)
        review_serializer.save()
        return Response(review_serializer.data, status=status.HTTP_200_OK)
        
    # 삭제
    def delete(self, request, obj_id): # 댓글 id 받아옴
        
        try:
            review_delete = ReviewModel.objects.get(obj_id)  
        except ProductModel.DoesNotExist:
         # some event						   status=400
            return Response({"message": "오브젝트가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        review_delete.delete()
        # 오브젝트, data , partial 넘기기
        return Response({"message": f"{ReviewModel.username} 정보가 더 이상 존재하지 않습니다."}, status=status.HTTP_200_OK)



class LikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'cart.html'

    def post(request, obj_id): # product obj_id
        if request.user.is_authenticated:
            product = get_object_or_404(ProductModel, obj_id)

            if product.like.filter(request.user_id).exists():
                product.like.remove(request.user)
            else:
                product.like_users.add(request.user)
            return Response({"message": f"{ReviewModel.product.title}에 좋아요 하셨습니다."}, status=status.HTTP_200_OK)
        return Response({"message": "로그인 한 유저만 좋아요가 가능합니다."}, status=status.HTTP_400_BAD_REQUEST)