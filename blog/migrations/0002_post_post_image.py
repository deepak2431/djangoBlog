# Generated by Django 2.2.8 on 2019-12-09 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_image',
            field=models.ImageField(null=True, upload_to='post_images/'),
        ),
    ]
