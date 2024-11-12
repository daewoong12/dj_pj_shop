# Generated by Django 4.1.7 on 2023-04-03 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("mall", "0023_alter_order_list"),
    ]

    operations = [
        migrations.RemoveField(model_name="order", name="list",),
        migrations.AddField(
            model_name="order", name="quantity", field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="order",
            name="stuff",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, to="mall.stuff"
            ),
            preserve_default=False,
        ),
    ]