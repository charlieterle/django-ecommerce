import uuid
import datetime
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver

class CustomUser(AbstractUser):
    family_name = models.CharField(max_length=40, verbose_name='お名前（姓）')
    given_name = models.CharField(max_length=40, verbose_name='お名前（名）')

    # first_nameとlast_nameをオーバーライド
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
        verbose_name="商品名"
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="商品の一意の識別子",
    )

    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="売り手",
    )

    created_at = models.DateTimeField(
        default=now,
        verbose_name='作成日時',
        null=False,
    )

    price = models.PositiveBigIntegerField(default=0, verbose_name="値段")  # JPY(円)で表します

    SALE_STATUS = (
        ("f", "販売中"),
        ("s", "販売済み"),
        ("c", "販売確定"),
    )
    status = models.CharField(
        max_length=1,
        choices=SALE_STATUS,
        default="f",
        verbose_name="販売ステータス"
    )

    info = models.TextField(
        max_length=3000,
        null=True,
        blank=True,
        verbose_name="商品の詳細",
    )

    def __str__(self):
        """商品を表す文字列"""
        return self.name

    def get_absolute_url(self):
        """特定の商品へのURLをリターンする関数"""
        return reverse("product-detail", args=[str(self.id)])

    class Meta:
        permissions = [("vendor_status", "売り手です")]
        verbose_name = "商品"
        verbose_name_plural = "商品"


def user_directory_path(instance, filename):
    """ユーザー名のファイルパスをURL化する関数"""
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    return 'vendor_{0}/{1}/{2}/{3}/{4}'.format(instance.product.vendor.id, year, month, day, filename)

def user_image_directory_path(instance, filename):
    """user_directory_pathに images/ を追加する関数"""
    return "images/" + user_directory_path(instance, filename)

class Image(models.Model):
    """画像を表すモデル"""

    product = models.ForeignKey(
        Product,
        default=None,
        on_delete=models.CASCADE,
    )

    image = models.ImageField(
        upload_to=user_image_directory_path,
    )

    class Meta:
        verbose_name = "画像"
        verbose_name_plural = "画像"
