from rest_framework import serializers

from django.db.models import F, Q, Avg, Max

from userchoice.models import Review as ReviewModel
from userchoice.models import Like as LikeModel
from userchoice.models import Cart as CartModel

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
        fields = ["user", "product", "pay_check", "delivery_state", ]
