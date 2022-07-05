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
from userchoice.models import Cart as CartModel
from userchoice.models import OrderList as OrderListModel
from product.models import Product as ProductModel
from product.models import Category as CategoryModel
from user.models import User as UserModel

from userchoice.serializers import CartSerializer, OrderListSerializer, ReviewSerializer

class CartView(APIView):
    
    def get(self, request):
        # user = request.user
        user = UserModel.objects.get(id=2)
        cart = CartModel.objects.filter(user=user)
        # user = UserModel.objects.all().order_by('?').first()
        print(cart)
        serialized_cart_data = CartSerializer(cart, many=True).data # 오브젝트를 넣어서 직렬화해주기
        print(serialized_cart_data)
        return Response(serialized_cart_data, status=status.HTTP_200_OK)

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
            return Response(cart_serializer.data, status=status.HTTP_200_OK)
        print('4')
        return Response(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
    # 장바구니 수정
    def put(self, request, obj_id):
        
        # user_update = UserModel.objects.get(id=obj_id)
        cart_update = CartModel.objects.get(id=obj_id)
        # 오브젝트, data , partial 넘기기
        cart_serializer = CartSerializer(cart_update, data=request.data, partial=True)
        cart_serializer.is_valid(raise_exception=True)
        cart_serializer.save() # 정상
        return Response(cart_serializer.data, status=status.HTTP_200_OK)
    

    # 장바구니삭제
    def delete(self, request, obj_id):
        
        try:
            # user_delete = UserModel.objects.get(obj_id)
            cart_delete = CartModel.objects.get(id=obj_id)
        except CartModel.DoesNotExist:
         # some event						   status=400
            return Response({"message": "장바구니가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        # cart_serializer = CartSerializer(cart_delete, data=request.data, partial=True)
        cart_delete.delete()
        # 오브젝트, data , partial 넘기기
        return Response({"message": f"{CartModel.product} 정보가 더 이상 존재하지 않습니다."}, status=status.HTTP_200_OK)

class OrderListView(APIView):
    
    # 구매내역 조회
    def get(self, request):
        # user = request.user
        user = UserModel.objects.get(id=1)
        order_list = OrderListModel.objects.filter(user=user)
        # user = UserModel.objects.all().order_by('?').first()
        print(order_list)
        serialized_order_list_data = OrderListSerializer(order_list, many=True).data
        print(serialized_order_list_data)
        return Response(serialized_order_list_data, status=status.HTTP_200_OK)


    # 장바구니에 있는 것들 구매하기
    def post(self, request):
        '''
        사용자 정보를 입력받아 create 하는 함수
        '''
        # cart = CartModel.objects.get(user_id=request.user.id)
        # cart = CartModel.objects.filter(user_id=1)
        # order_list = OrderListModel.objects.all().order_by('?').first()
        # print(cart)
        # print(order_list)
        print('0')
        order_list_serializer = OrderListSerializer(data=request.data)
        
        print('1')
        if order_list_serializer.is_valid():
            print('2')
            order_list_serializer.save() # 정상
            print('3')
            print(order_list_serializer.data)
            print(request.data)
            cart_lists = request.data.get('get_carts')
            for i in cart_lists:
                cart = CartModel.objects.filter(is_paid=True)
                cart.delete()
            return Response(order_list_serializer.data, status=status.HTTP_200_OK)
        print('4')
        return Response(order_list_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # 구매내역 수정(고객정보, 배송지정보, 배송상태 등등)
    def put(self, request, obj_id):
        
        # user_update = UserModel.objects.get(id=obj_id)
        order_list_update = OrderListModel.objects.get(id=obj_id)
        # 오브젝트, data , partial 넘기기
        order_list_serializer = OrderListSerializer(order_list_update, data=request.data, partial=True)
        order_list_serializer.is_valid(raise_exception=True)
        order_list_serializer.save() # 정상
        return Response(order_list_serializer.data, status=status.HTTP_200_OK)
        
    # 구매내역 삭제
    def delete(self, request, obj_id):
        
        try:
            # user_delete = UserModel.objects.get(obj_id)
            order_list_delete = OrderListModel.objects.get(id=obj_id)
        except OrderListModel.DoesNotExist:
         # some event						   status=400
            return Response({"message": "구매내역이 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        order_list_delete.delete()
        # 오브젝트, data , partial 넘기기
        return Response({"message": f"{OrderListModel.cart} 정보가 더 이상 존재하지 않습니다."}, status=status.HTTP_200_OK)


#상품별로처리
class ReviewView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    
    #상품별로 상품에 대해서 review 정보 가져오고
    permission_classes = [permissions.AllowAny]
    def get(self, request, obj_id):  # 상품 id 받아옴
        # product = ProductModel.objects.get(id=obj_id)
        # data = request.data.dict()
        # data['product'] = obj_id
        reviews = ReviewModel.objects.filter(product_id=obj_id)
        # product = ProductModel.objects.all().order_by('?').first()
        print(reviews)
        serialized_review_data = ReviewSerializer(reviews, many=True).data # 오브젝트를 넣어서 직렬화해주기
        print(serialized_review_data)
        print(type(serialized_review_data))
        return Response(serialized_review_data, status=status.HTTP_200_OK)

    # 상품 리뷰 등록
    def post(self, request): # 상품 id 받아옴
        '''
        상품 정보를 입력받아 review create 하는 함수
        '''
        review_serializer = ReviewSerializer(data=request.data)
        print(review_serializer)
        if review_serializer.is_valid():
            print('1')
            review_serializer.save() # 정상
            return Response(review_serializer.data, status=status.HTTP_200_OK)

        return Response(review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
    # 상품 리뷰 수정
    def put(self, request, obj_id): # 댓글 id 받아옴
        
        product_review_info_change = ReviewModel.objects.get(product_id=obj_id)
        # 오브젝트, data , partial 넘기기
        review_serializer = ReviewSerializer(product_review_info_change, data=request.data, partial=True)
        review_serializer.is_valid(raise_exception=True)
        review_serializer.save()
        return Response(review_serializer.data, status=status.HTTP_200_OK)
        
    # 삭제
    def delete(self, request, obj_id): # 댓글 id 받아옴
        
        try:
            review_delete = ReviewModel.objects.get(id=obj_id)
            print('1')
        except ProductModel.DoesNotExist:
         # some event						   status=400
            print('2')
            return Response({"message": "오브젝트가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        print('3')
        review_delete.delete()
        print('4')
        # 오브젝트, data , partial 넘기기
        return Response({"message": "해당 댓글 정보가 더 이상 존재하지 않습니다."}, status=status.HTTP_200_OK)
        # return Response({"message": f"{request.user.fullname}님의 해당 댓글 정보가 더 이상 존재하지 않습니다."}, status=status.HTTP_200_OK)


class LikeView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(request, obj_id): # product obj_id
        if request.user.is_authenticated:
            product = get_object_or_404(ProductModel, obj_id)

            if product.like.filter(request.user_id).exists():
                product.like.remove(request.user)
            else:
                product.product_like.add(request.user)
            return Response({"message": f"{ReviewModel.product.title}에 좋아요 하셨습니다."}, status=status.HTTP_200_OK)
        return Response({"message": "로그인 한 유저만 좋아요가 가능합니다."}, status=status.HTTP_400_BAD_REQUEST)