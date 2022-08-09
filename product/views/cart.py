from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import get_object_or_404
# from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User as UserModel

from product.models import Cart as CartModel
from product.serializers import CartSerializer
# from utils.permissions import IsCustomer

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
