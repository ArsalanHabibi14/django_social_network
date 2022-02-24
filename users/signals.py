from . import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=models.Profile)
def created(sender, instance, created, **kwargs):
    if created:
        user = instance
        order = models.Order.objects.create(
            owner=user
        )
        order_following = models.OrderFollowing.objects.create(
            owner=user
        )
def create_profile(sender, instance, created, **kwargs):
	if created:
		user = instance
		profile = models.Profile.objects.create(
			user=user,
			user_name=user.username,
			last_name=user.last_name,
			email=user.email,
			password=user.password
		)
post_save.connect(create_profile, sender=User)
