# Generated by Django 4.1.7 on 2023-04-01 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mall", "0011_alter_cart_quantity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart", name="quantity", field=models.JSONField(default=dict),
        ),
    ]
