import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.conf import settings


class User(AbstractUser):
    given_name = models.CharField(max_length=40)
    family_name = models.CharField(max_length=40)

    # first_name と last_name をオーバーライド
    first_name = None
    last_name = None

    REQUIRED_FIELDS = ["email", "given_name", "family_name"]

    def __str__(self):
        return self.username


class Product(models.Model):
    """商品を表すモデル"""

    name = models.CharField(
        max_length=200,
        default="商品名未定義",
        help_text="商品名を入力してください",
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="全商品の中にこの商品の一意の識別子",
    )

    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    price = models.PositiveBigIntegerField(default=0)  # JPY(円)で表します

    SALE_STATUS = (
        ("f", "販売中"),
        ("s", "販売済み"),
        ("c", "販売確定"),
    )
    status = models.CharField(
        max_length=1,
        choices=SALE_STATUS,
        default="f",
        help_text="商品の販売ステータス",
    )

    info = models.CharField(
        max_length=3000,
        help_text="商品の詳細",
        null=True,
        blank=True,
    )

    def __str__(self):
        """商品を表す文字列"""
        return self.name

    def get_absolute_url(self):
        """特定の商品へのURLをリターンする関数"""
        return reverse("product-detail", args=[str(self.id)])

    class Meta:
        permissions = [("vendor_status", "売り手です")]
        default_permissions = ("add", "change", "view")
        # TODO deleteパーミッションを実装する。売り手は自分の商品しか削除できないように
