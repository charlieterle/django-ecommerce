# Generated by Django 5.1.4 on 2025-02-08 03:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0009_remove_customuser_first_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="family_name",
            field=models.CharField(max_length=40, verbose_name="お名前（姓）"),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="given_name",
            field=models.CharField(max_length=40, verbose_name="お名前（名）"),
        ),
        migrations.AlterField(
            model_name="product",
            name="info",
            field=models.TextField(
                blank=True, max_length=3000, null=True, verbose_name="商品の詳細"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="name",
            field=models.CharField(
                default="商品名未定義",
                help_text="商品名を入力してください",
                max_length=200,
                verbose_name="商品名",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.PositiveBigIntegerField(default=0, verbose_name="値段"),
        ),
        migrations.AlterField(
            model_name="product",
            name="vendor",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="売り手",
            ),
        ),
    ]
