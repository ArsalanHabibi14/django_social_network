# Generated by Django 3.2.7 on 2022-02-01 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_profile_is_active'),
        ('MGN', '0006_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationFollower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(choices=[('follow', 'Follow'), ('comment', 'Comment')], max_length=120)),
                ('description', models.TextField()),
                ('order_follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
    ]
