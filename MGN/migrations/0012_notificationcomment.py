# Generated by Django 3.2.7 on 2022-02-01 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20220201_1438'),
        ('users', '0021_profile_is_active'),
        ('MGN', '0011_auto_20220201_2009'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='posts.posts')),
                ('send_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SendUser', to='users.profile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
    ]
