# Generated by Django 3.2.7 on 2022-02-04 16:58

from django.db import migrations, models
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20220201_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=posts.models.upload_file),
        ),
    ]
