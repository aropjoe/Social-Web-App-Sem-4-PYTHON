# Generated by Django 2.1.5 on 2019-01-18 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_registration', '0004_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, upload_to='media/profile_pic'),
        ),
    ]
