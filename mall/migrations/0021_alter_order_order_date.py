# Generated by Django 4.1.7 on 2023-04-03 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mall", "0020_rename_total_order_subtotal"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order", name="order_date", field=models.DateTimeField(),
        ),
    ]
