from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from rest_framework_simplejwt.authentication import JWTAuthentication

from product.models import Product as ProductModel
from product.models import Review as ReviewModel


class LikeView(APIView):
    # permission_classes = [IsAdminOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def post(self, request, obj_id): # product obj_id
        if request.user.is_authenticated:
            product = get_object_or_404(ProductModel, obj_id)

            if product.like.filter(request.user_id).exists():
                product.like.remove(request.user)
            else:
                product.product_like.add(request.user)
            return Response({"message": f"{ReviewModel.product.title}에 좋아요 하셨습니다."}, status=status.HTTP_200_OK)
        return Response({"message": "로그인 한 유저만 좋아요가 가능합니다."}, status=status.HTTP_400_BAD_REQUEST)