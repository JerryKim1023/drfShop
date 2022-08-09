import os

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from django.utils import timezone
from rest_framework import permissions
# from rest_framework_simplejwt.authentication import JWTAuthentication

from django.views.static import serve


from product.models import Product as ProductModel
from product.models import Category as CategoryModel
from product.serializers import ProductSerializer
# from product.serializers import CategorySerializer
# from utils.permissions import IsAdminOrReadOnly, IsStaffOrReadOnly



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
        print(product_serializer)
        print(type(product_serializer))
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
        print('1')
        try:
            product_delete = ProductModel.objects.get(id=obj_id)
            print('2')
        except ProductModel.DoesNotExist:
         # some event						   status=400
            return Response({"message": "오브젝트가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        print('3')
        product_delete.delete()
        print('4')
        # 오브젝트, data , partial 넘기기
        return Response({"message": f"{ProductModel.user.username} 정보가 더 이상 존재하지 않습니다."}, status=status.HTTP_200_OK)

class ProductThumbnailView(APIView):
    permission_classes = []

    def get(self, request, obj_id):
        product = ProductModel.objects.get(id=obj_id)
        file_path = product.thumbnail.path
        return serve(request, os.path.basename(file_path), os.path.dirname(file_path))
            # 스태틱파일(이미지 파일 등등) 을 serve(보내준다)해준다.