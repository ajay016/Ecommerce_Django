# Generated by Django 4.1.1 on 2022-11-17 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0005_rename_name_customer_first_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]
