# Generated by Django 4.1.1 on 2023-04-28 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_userprofile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='../static/user-profile-avatar6.png', null=True, upload_to=''),
        ),
    ]
