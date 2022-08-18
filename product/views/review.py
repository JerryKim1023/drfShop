from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product as ProductModel
from product.models import Review as ReviewModel
from product.serializers import ReviewSerializer
from utils.permissions import IsCustomer



class ReviewByProduct(APIView):
    permission_classes = [permissions.AllowAny]
    #상품별로 상품에 대해서 review 정보 가져오고

    def get(self, request, id):  # 상품 id 받아옴
        # product = ProductModel.objects.get(id=obj_id)
        # data = request.data.dict()
        # data['product'] = obj_id
        reviews = ReviewModel.objects.filter(product_id=id)
        # product = ProductModel.objects.all().order_by('?').first()
        print(reviews)
        serialized_review_data = ReviewSerializer(reviews, many=True).data # 오브젝트를 넣어서 직렬화해주기
        print(serialized_review_data)
        print(type(serialized_review_data))
        return Response(serialized_review_data, status=status.HTTP_200_OK)

class ReviewWrite(APIView):
    permission_classes = [IsCustomer]
    
    # 상품 리뷰 등록
    def post(self, request): # 상품 id 받아옴
        '''
        상품 정보를 입력받아 review create 하는 함수
        '''
        review_serializer = ReviewSerializer(data=request.data)
        print(review_serializer)
        if review_serializer.is_valid():
            print('1')
            review_serializer.save() # 정상
            return Response(review_serializer.data, status=status.HTTP_200_OK)

        return Response(review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewChangeDelete(APIView):
    permission_classes = [IsCustomer]
    
    # 상품 리뷰 수정
    def put(self, request, obj_id): # 댓글 id 받아옴
        
        product_review_info_change = ReviewModel.objects.get(product_id=obj_id)
        # 오브젝트, data , partial 넘기기
        review_serializer = ReviewSerializer(product_review_info_change, data=request.data, partial=True)
        review_serializer.is_valid(raise_exception=True)
        review_serializer.save()
        return Response(review_serializer.data, status=status.HTTP_200_OK)
        
    # 삭제
    def delete(self, request, obj_id): # 댓글 id 받아옴
        
        try:
            review_delete = ReviewModel.objects.get(id=obj_id)
            print('1')
        except ProductModel.DoesNotExist:
         # some event						   status=400
            print('2')
            return Response({"message": "오브젝트가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        print('3')
        review_delete.delete()
        print('4')
        # 오브젝트, data , partial 넘기기
        return Response({"message": "해당 댓글 정보가 더 이상 존재하지 않습니다."}, status=status.HTTP_200_OK)
        # return Response({"message": f"{request.user.fullname}님의 해당 댓글 정보가 더 이상 존재하지 않습니다."}, status=status.HTTP_200_OK)
