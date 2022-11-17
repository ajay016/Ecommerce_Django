# Generated by Django 4.1.1 on 2022-11-16 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0004_shippingaddress_phone"),
    ]

    operations = [
        migrations.RenameField(
            model_name="customer", old_name="name", new_name="first_name",
        ),
        migrations.RemoveField(model_name="shippingaddress", name="phone",),
        migrations.AddField(
            model_name="customer",
            name="last_name",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="customer",
            name="phone",
            field=models.CharField(max_length=200, null=True),
        ),
    ]
