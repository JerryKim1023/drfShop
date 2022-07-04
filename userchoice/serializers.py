from rest_framework import serializers

from django.db.models import F, Q, Avg, Max

from userchoice.models import Review as ReviewModel
from userchoice.models import Like as LikeModel
from userchoice.models import Cart as CartModel
from userchoice.models import OrderList as OrderListModel

from datetime import datetime, timedelta
from django.utils import timezone

class ReviewSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()

    # def get_user(self, obj):
        
    #     return obj.user.fullname

    class Meta:
        # serializer에 사용될 model, field지정
        model = ReviewModel
        # 모든 필드를 사용하고 싶을 경우 fields = "__all__"로 사용
        fields = ["user", "product", "content", "created", "rating", ]

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.fullname

    class Meta:
        # serializer에 사용될 model, field지정
        model = LikeModel
        # 모든 필드를 사용하고 싶을 경우 fields = "__all__"로 사용
        fields = ["user", "product_like", ]


class CartSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()

    # def get_user(self, obj):
    #     return obj.user.fullname

    class Meta:
        # serializer에 사용될 model, field지정
        model = CartModel
        # 모든 필드를 사용하고 싶을 경우 fields = "__all__"로 사용
        fields = ["user", "product", "product_option",]


class OrderListSerializer(serializers.ModelSerializer):
    cart = CartSerializer(many=True, required=False)
    get_carts = serializers.ListField(required=False) # 리스트 필드로 지정해서 리스트 포맷으로 받을 수 있게 됨.
    class Meta:
        # serializer에 사용될 model, field지정
        model = OrderListModel
        # 모든 필드를 사용하고 싶을 경우 fields = "__all__"로 사용
        fields = ["user", "the_time_payed", "complete", "pay_check", "delivery_state", "cart", "get_carts",]

    def create(self, validated_data):
        print(validated_data)
        get_carts = validated_data.pop("get_carts", []) # 앞의 값 가져와서 없으면 [] 로 넘겨줌.
        print(get_carts)
        order_list = OrderListModel(**validated_data)
        print(order_list)
        order_list.save()

        # cart 등록
        order_list.cart.add(*get_carts) # M2M 관계여서 .add 가 가능
        order_list.save()

        # cart 내역은 삭제
        for i in get_carts:
            purchased_cart = OrderListModel.objects.filter(cart_id=i)
            purchased_cart.delete()

        return order_list

    def update(self, instance, validated_data): # 기본 업데이트 함수 구현해서 위로 커스텀
        # 인스턴스에는 입력된 오브젝트가 담긴다.
        print(instance)
        print(validated_data)
        for key, value in validated_data.items():
            if key == "desc":
                created = getattr(instance, key).split("\n")[-1]
                value += f"\n\n{created}"
            setattr(instance, key, value) # instance.key = value 이렇게 매핑 시켜주는 로직

        instance.desc = f"{instance.modified.replace(microsecond=0, tzinfo=None)}에 수정되었습니다.\n\n"\
                                  + instance.desc

        instance.save()
        return instance
