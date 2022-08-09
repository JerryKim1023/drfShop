from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
# from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User as UserModel

from product.models import OrderList as OrderListModel
from product.models import Cart as CartModel
from product.serializers import OrderListSerializer
# from utils.permissions import IsCustomer



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

