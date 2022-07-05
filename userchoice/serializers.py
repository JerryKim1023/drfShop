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
    # user = serializers.SerializerMethodField()

    # def get_user(self, obj):
    #     return obj.user.fullname

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
        fields = ["user", "product", "product_option", "is_paid",]


class OrderListSerializer(serializers.ModelSerializer):
    cart = CartSerializer(many=True, required=False)
    get_carts = serializers.ListField(required=False)

    class Meta:
        model = OrderListModel
        fields = ["user", "the_time_payed", "pay_check", "delivery_state", "cart", "get_carts",]

    def create(self, validated_data):
        get_carts = validated_data.pop("get_carts", []) # 앞의 값 가져와서 없으면 [] 로 넘겨줌.
        order_list = OrderListModel(**validated_data)
        order_list.save()
        for i in get_carts:
            cart = CartModel.objects.get(id=i)
            cart.is_paid = True
            cart.save()
        # order_list.cart.is_paid = True
        
        order_list.cart.add(*get_carts)
        order_list.save()

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
