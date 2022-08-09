from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User as UserModel

from product.models import OrderList as OrderListModel
from product.serializers import OrderListSerializer
from utils.permissions import IsCustomer

class OrderListCreateAPI(APIView):
    permission_classes = [IsCustomer]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        order = OrderListModel.objects.filter(customer=request.user)
        serializer = OrderListSerializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrderListSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPI(APIView):
    permission_classes = [IsCustomer]
    authentication_classes = [JWTAuthentication]

    def _get_object(self, id):
        order = get_object_or_404(OrderListModel, id=id)
        self.check_object_permissions(self.request, order)  # Check object level
        return order

    def get(self, request, id):
        order = self._get_object(id)
        serializer = OrderListSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        order = self._get_object(id)
        if order.status == "PAY_COMPLETE":
            order.delete()
            return Response({"MESSAGE": "주문이 취소되었습니다."}, status=status.HTTP_204_NO_CONTENT)
