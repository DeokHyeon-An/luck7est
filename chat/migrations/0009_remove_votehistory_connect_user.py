# Generated by Django 2.2 on 2022-05-16 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_auto_20220516_0608'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='votehistory',
            name='connect_user',
        ),
    ]
