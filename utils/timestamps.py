from django.db import models
from django.utils import timezone


class Timestamp(models.Model):
    created_at = models.DateTimeField("생성 일자", auto_now_add=True)
    updated_at = models.DateTimeField("수정 일자", auto_now=True)
    deleted_at = models.DateTimeField("삭제 일자", null=True)

    class Meta:
        abstract = True


class ActiveTime(Timestamp):
    is_active = models.BooleanField("활성화 여부", default=True)

    class Meta:
        abstract = True
