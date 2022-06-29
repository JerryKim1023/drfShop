import os
from unicodedata import category
from django.shortcuts import render
# views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status

from drfShop.permissions import UserSeller

from rest_framework.renderers import TemplateHTMLRenderer

from django.db.models import F

from django.views.static import serve

from datetime import datetime, timedelta, timezone
from product.models import Product as ProductModel
from product.models import ProductOption as ProductOptionModel
from product.models import Category as CategoryModel

from product.serializers import ProductSerializer 
from product.serializers import CategorySerializer
from userchoice.serializers import CartSerializer

# Create your views here.

# 상품에 대한 처리
class ProductItemView(APIView):
    
    #카테고리별 상품에 대해서 product 정보 가져오고
    # permission_classes = [UserSeller]
    permission_classes = [permissions.AllowAny] # 포스트맨 요청받기 위해 임시로 
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'sell_product.html'
    def get(self, request):
        product = ProductModel.objects.all()
        category = CategoryModel.objects.all().order_by('?').first() # 임시로 카테고리 랜덤으로 하나 뽑아오게함.
        
        product_serializer = ProductSerializer(product, many=True)

        # if not True :
        #     return Response(status=status.HTTP_401_UNAUTHORIZED) # template_name = 'index.html', 
        return Response(product_serializer.data, status=status.HTTP_200_OK) #  template_name = 'sell_product.html',

        # return data example
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
        
        product_sale_serializer = ProductSerializer(data=request.data, partial=True)
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



class CategoryView(APIView):
    
    #해당 카테고리에 대한 product 정보 가져오고
    # permission_classes = [UserSeller]
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'sell_product.html'

    def get(self, request, obj_id):    # 카테고리 id
        category = CategoryModel.objects.get(obj_id)
        serialized_product_data = ProductSerializer(category).data # 오브젝트를 넣어서 직렬화해주기
        return Response(serialized_product_data, status=status.HTTP_200_OK) # , template_name = 'sell_product.html'

        # return data
        """
        {
            "username": "user",
            "password": "pbkdf2_sha256$320000$u5YnmKo9luab9csqWpzRsa$pKfqHnBiF5Rgdo1Mj9nxNOdhpAl9AhPVXFPXkbPz7Mg=",
            "fullname": "user's name",
            "email": "user@email.com"
        }
        """

    # 카테고리 생성
    def post(self, request):
        '''
        상품 정보를 입력받아 create 하는 함수
        '''
        print('1')
        category_serializer = CategorySerializer(data=request.data)
        print(category_serializer)
        if category_serializer.is_valid(): 
            print('3')
            category_serializer.save() # 정상
            print('4')
            return Response(category_serializer.data, template_name = 'sell_product.html', status=status.HTTP_200_OK)
        print('5')
        return Response(category_serializer.errors, template_name = 'sell_product.html', status=status.HTTP_400_BAD_REQUEST)
      
    # 카테고리 수정
    def put(self, request, obj_id):   # 카테고리 id
        category = CategoryModel.objects.get(obj_id)
        # 오브젝트, data , partial 넘기기
        category_serializer = CategorySerializer(category, data=request.data, partial=True)
        category_serializer.is_valid(raise_exception=True)
        category_serializer.save()
        return Response(category_serializer.data, status=status.HTTP_200_OK)
        
    # 삭제
    def delete(self, request, obj_id):
        
        try:
            category_delete = CategoryModel.objects.get(obj_id)  
        except CategoryModel.DoesNotExist:
         # some event						   status=400
            return Response({"message": "오브젝트가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        category_delete.delete()
        # 오브젝트, data , partial 넘기기
        return Response({"message": f"{CategoryModel.name} 정보가 더 이상 존재하지 않습니다."}, status=status.HTTP_200_OK)





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