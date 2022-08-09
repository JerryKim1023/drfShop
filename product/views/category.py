from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
# from rest_framework_simplejwt.authentication import JWTAuthentication

from product.models import Product as ProductModel
from product.models import Category as CategoryModel
from product.serializers import CategorySerializer, ProductSerializer
# from utils.permissions import IsAdminOrReadOnly


class CategoryView(APIView):
    
    #해당 카테고리에 대한 product 정보 가져오고
    # permission_classes = [UserSeller]
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'sell_product.html'


    def get(self, request, obj_id):    # 카테고리 id
        print('1')
        category_product = ProductModel.objects.filter(category_id=obj_id)
        print(category_product)
        # category = CategoryModel.objects.all().order_by('?').first() # 임시로 카테고리 랜덤으로 하나 뽑아오게함.
        print('3')
        serialized_product_data = ProductSerializer(category_product, many=True).data # 오브젝트를 넣어서 직렬화해주기
        print(serialized_product_data)
        print(type(serialized_product_data))
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
            print(category_serializer)
            category_serializer.save() # 정상
            print(category_serializer.data)
            return Response(category_serializer.data, status=status.HTTP_200_OK)
        print('5')
        return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
    # 카테고리 수정
    def put(self, request, obj_id):   # 카테고리 id
        category = CategoryModel.objects.get(id=obj_id)
        print(category)
        # 오브젝트, data , partial 넘기기
        category_serializer = CategorySerializer(category, data=request.data, partial=True)
        print(category_serializer)
        category_serializer.is_valid(raise_exception=True)
        category_serializer.save()
        return Response(category_serializer.data, status=status.HTTP_200_OK)
        
    # 삭제
    def delete(self, request, obj_id):
        
        try:
            category_delete = CategoryModel.objects.get(id=obj_id)  
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
