from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication

from product.models import Category as CategoryModel
from product.serializers import CategorySerializer
from utils.permissions import IsAdminOrReadOnly

class CategoryListCreateAPI(APIView):
    permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        categories = CategoryModel.objects.filter(is_active=True)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailAPI(APIView):
    permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def _get_object(self, id):
        category = get_object_or_404(CategoryModel, id=id)
        return category

    def get(self, request, id):
        category = self._get_object(id)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, id):
        category = self._get_object(id)
        serializer = CategorySerializer(category, data=request.data, partial=True)  # 부분수정 가능
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        category = self._get_object(id)
        category.is_active = False
        category.deleted_at = datetime.now()
        category.save()
        return Response(status=status.HTTP_204_NO_CONTENT)





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
