# Generated by Django 5.1.4 on 2024-12-30 05:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("admin", "0003_logentry_add_action_flag_choices"),
        ("catalog", "0002_ecommerceuser_alter_product_options_product_info_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="EcommerceUser",
            new_name="User",
        ),
    ]
