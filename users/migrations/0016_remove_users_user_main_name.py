# Generated by Django 3.2.7 on 2022-01-29 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_users_user_main_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='user_main_name',
        ),
    ]
