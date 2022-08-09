from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User as UserModel

from product.models import Cart as CartModel
from product.serializers import CartSerializer
from utils.permissions import IsCustomer

class CartListCreateAPI(APIView):
    permission_classes = [IsCustomer]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        cart = CartModel.objects.filter(buy=False, customer=request.user)
        serializer = CartSerializer(cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CartSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartDetailAPI(APIView):
    permission_classes = [IsCustomer]
    authentication_classes = [JWTAuthentication]

    def _get_object(self, id):
        cart = get_object_or_404(CartModel, id=id)
        self.check_object_permissions(self.request, cart) # Check object level
        return cart

    def get(self, request, id):
        cart = self._get_object(id)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        cart = self._get_object(id)
        serializer = CartSerializer(cart, data=request.data, partial=True)  # 부분수정 가능
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        cart = self._get_object(id)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
