# Generated by Django 4.1.1 on 2022-09-29 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0002_shippingaddress_orderitem"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
    ]
