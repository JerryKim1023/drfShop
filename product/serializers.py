from rest_framework import serializers

from django.db.models import F, Q, Avg, Max

from product.models import Product as ProductModel
from product.models import ProductOption as ProductOptionModel
from product.models import Category as CategoryModel

from datetime import datetime, timedelta
from django.utils import timezone

from userchoice.serializers import ReviewSerializer

class ProductSerializer(serializers.ModelSerializer):
    product_option = serializers.SerializerMethodField()
    review = serializers.SerializerMethodField()
    def get_review(self, obj):
        reviews = obj.review_set
        return {
            "last_review": ReviewSerializer(reviews.last()).data,
            "average_rating": reviews.aggregate(avg=Avg("rating"))["avg"]
        }

    def validate(self, data):
        show_expired_date = data.get("show_expired_date", "")
        if show_expired_date and show_expired_date < datetime.now().date():
            raise serializers.ValidationError(
                detail={"error": "유효하지 않은 노출 종료 날짜입니다."},
            )
        return data

    def create(self, validated_data):
        product = ProductModel(**validated_data)
        product.user = self.context['request'].user
        product.save()
        product.desc += f"\n\n{product.created.replace(microsecond=0, tzinfo=None)}에 등록된 상품입니다."
        product.save()

        return product

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

    class Meta:
        # serializer에 사용될 model, field지정
        model = ProductModel
        # 모든 필드를 사용하고 싶을 경우 fields = "__all__"로 사용
        fields = ["user", "category", "title", "thumbnail", "desc", "created", 
                  "modified", "show_expired_date", "stock", "is_active", "product_option", "review"]


class ProductOptionSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    def get_product(self, obj):
        return obj.product.title

    class Meta:
        # serializer에 사용될 model, field지정
        model = ProductOptionModel
        # 모든 필드를 사용하고 싶을 경우 fields = "__all__"로 사용
        fields = ["product", "name", "quantity", "size", "price", ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        # serializer에 사용될 model, field지정
        model = CategoryModel
        # 모든 필드를 사용하고 싶을 경우 fields = "__all__"로 사용
        fields = "__all__"
