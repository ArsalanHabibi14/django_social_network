# Generated by Django 3.2.7 on 2022-01-25 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20220125_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_follower',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
