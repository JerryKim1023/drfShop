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
from product.models import Product as ProductModel
from product.models import ProductOption as ProductOptionModel
from product.models import Category as CategoryModel

from product.serializers import ProductSerializer
from userchoice.serializers import CartSerializer

# Create your views here.

# 모든 상품에 대한 처리
class ProductItemView(APIView):
    
    #모든 상품에 대해서 product 정보 가져오고
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        product = ProductModel.objects.all()
        serialized_product_data = ProductSerializer(product).data # 오브젝트를 넣어서 직렬화해주기
        return Response(serialized_product_data, many=True, status=status.HTTP_200_OK)

        # return data
        """
        {
            "username": "user",
            "password": "pbkdf2_sha256$320000$u5YnmKo9luab9csqWpzRsa$pKfqHnBiF5Rgdo1Mj9nxNOdhpAl9AhPVXFPXkbPz7Mg=",
            "fullname": "user's name",
            "email": "user@email.com"
        }
        """

    # 상품 등록
    def post(self, request):
        '''
        상품 정보를 입력받아 create 하는 함수
        '''
        product_sale_serializer = ProductSerializer(data=request.data)
        if product_sale_serializer.is_valid(): 
            product_sale_serializer.save() # 정상
            return Response(product_sale_serializer.data, status=status.HTTP_200_OK)

        return Response(product_sale_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
    # 상품 수정
    def put(self, request, obj_id):
        
        product_sale_info_change = ProductModel.objects.get(id=obj_id)
        # 오브젝트, data , partial 넘기기
        product_sale_update = ProductSerializer(product_sale_info_change, data=request.data, partial=True)
        product_sale_update.is_valid(raise_exception=True)
        product_sale_update.save()
        return Response(product_sale_update.data, status=status.HTTP_200_OK)
        
    # 삭제
    def delete(self, request, obj_id):
        
        try:
            product_delete = ProductModel.objects.get(obj_id)  
        except ProductModel.DoesNotExist:
         # some event						   status=400
            return Response({"message": "오브젝트가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        product_delete.delete()
        # 오브젝트, data , partial 넘기기
        return Response({"message": f"{ProductModel.username} 정보가 더 이상 존재하지 않습니다."}, status=status.HTTP_200_OK)

#카테고리별로처리
class ProductCategoryView(APIView):
    
    #카테고리별로 상품에 대해서 product 정보 가져오고
    permission_classes = [permissions.AllowAny]
    def get(self, request , obj_id):
        category = CategoryModel.get(obj_id)
        serialized_product_data = ProductSerializer(category).data # 오브젝트를 넣어서 직렬화해주기
        return Response(serialized_product_data, many=True, status=status.HTTP_200_OK)

        # return data
        """
        {
            "username": "user",
            "password": "pbkdf2_sha256$320000$u5YnmKo9luab9csqWpzRsa$pKfqHnBiF5Rgdo1Mj9nxNOdhpAl9AhPVXFPXkbPz7Mg=",
            "fullname": "user's name",
            "email": "user@email.com"
        }
        """

    # 상품 등록
    def post(self, request):
        '''
        상품 정보를 입력받아 create 하는 함수
        '''
        product_sale_serializer = ProductSerializer(data=request.data)
        if product_sale_serializer.is_valid(): 
            product_sale_serializer.save() # 정상
            return Response(product_sale_serializer.data, status=status.HTTP_200_OK)

        return Response(product_sale_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
    # 상품 수정
    def put(self, request, obj_id):
        
        product_sale_info_change = ProductModel.objects.get(id=obj_id)
        # 오브젝트, data , partial 넘기기
        product_sale_update = ProductSerializer(product_sale_info_change, data=request.data, partial=True)
        product_sale_update.is_valid(raise_exception=True)
        product_sale_update.save()
        return Response(product_sale_update.data, status=status.HTTP_200_OK)
        
    # 삭제
    def delete(self, request, obj_id):
        
        try:
            product_delete = ProductModel.objects.get(obj_id)  
        except ProductModel.DoesNotExist:
         # some event						   status=400
            return Response({"message": "오브젝트가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        product_delete.delete()
        # 오브젝트, data , partial 넘기기
        return Response({"message": f"{ProductModel.username} 정보가 더 이상 존재하지 않습니다."}, status=status.HTTP_200_OK)

# 특정 아이템에 대한 처리
class ProductDetailView(APIView):
    
    #해당 상품에 대해서 product 정보 가져오고
    permission_classes = [permissions.AllowAny]
    def get(self, request, obj_id):
        product = ProductModel.objects.get(obj_id)
        serialized_product_data = ProductSerializer(product).data # 오브젝트를 넣어서 직렬화해주기
        return Response(serialized_product_data, status=status.HTTP_200_OK)

        # return data
        """
        {
            "username": "user",
            "password": "pbkdf2_sha256$320000$u5YnmKo9luab9csqWpzRsa$pKfqHnBiF5Rgdo1Mj9nxNOdhpAl9AhPVXFPXkbPz7Mg=",
            "fullname": "user's name",
            "email": "user@email.com"
        }
        """

    # 상품 구매 옵션 정보를 받아서 장바구니에 넣어주기
    def post(self, request):
        '''
        상품 정보를 입력받아 create 하는 함수
        '''
        user_purhase_option = ProductOptionModel.objects.create(**request.data)
        product_purchase_serializer = ProductSerializer(user_purhase_option, data=request.data)
        cart_serializer = CartSerializer(id=request.user_id, data=product_purchase_serializer) # 이렇게 프로덕트 정보를 담아줘도 되나...
        if cart_serializer.is_valid(): 
            cart_serializer.save() # 정상
            return Response(cart_serializer.data, status=status.HTTP_200_OK)

        return Response(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
    # 구매정보 수정
    def put(self, request, obj_id):
        
        product_update = ProductModel.objects.get(id=obj_id)
        # 오브젝트, data , partial 넘기기
        product_serializer = ProductSerializer(product_update, data=request.data, partial=True)
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save()
        return Response(product_serializer.data, status=status.HTTP_200_OK)
        
    # 삭제
    def delete(self, request, obj_id):
        
        try:
            product_delete = ProductModel.objects.get(obj_id)  
        except ProductModel.DoesNotExist:
         # some event						   status=400
            return Response({"message": "오브젝트가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        product_delete.delete()
        # 오브젝트, data , partial 넘기기
        return Response({"message": f"{ProductModel.username} 정보가 더 이상 존재하지 않습니다."}, status=status.HTTP_200_OK)






# 1. 회원가입 기능 (일반 사용자 / 판매자 별로 나누기) -> user

# 2. 카테고리 별 상품 등록/제거/조회/수정 기능 (모델에 존재하는 카테고리만 선택 가능)
# 3. 상품 별 리뷰 등록/제거/조회/수정 기능
# 4. 상품 찜하기 기능
# 5. 상품 구매 시 옵션 선택 기능 (색상 / 사이즈 등 선택 가능하도록)
# 6. 상품 장바구니 담기 버튼 누르면 장바구니에 담기는 기능
# 7. 장바구니에서 결제하면 자신이 구매한 상품 목록/상태 조회 기능 (구매자는 상태 조회만, 판매자는 제품 배송 상태 변경 가능하도록)
# 8. 일반 사용자 (구매자) / 판매자 / 관리자 별 권한 나누기
# 9. 관리자 페이지 별도 생성해서, 유저 데이터 및 구매 로그 등을 모두 볼 수 있도록 하기
    
#     (+ 판매자가 가입 신청 시, 관리자가 승인을 해야 가입이 완료되도록 하기)

class ProductThumbnailView(APIView):
    permission_classes = []

    def get(self, request, obj_id):
        product = ProductModel.objects.get(id=obj_id)
        file_path = product.thumbnail.path
        return serve(request, os.path.basename(file_path), os.path.dirname(file_path))
            # 스태틱파일(이미지 파일 등등) 을 serve(보내준다)해준다.