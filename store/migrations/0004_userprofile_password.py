# Generated by Django 4.1.1 on 2023-04-26 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='password',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]