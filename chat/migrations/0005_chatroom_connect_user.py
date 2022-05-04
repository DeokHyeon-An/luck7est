# Generated by Django 2.2 on 2022-04-28 11:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20220424_0929'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='connect_user',
            field=models.ManyToManyField(blank=True, related_name='connect_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
