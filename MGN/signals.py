from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import MessageOrder, Messages
from users import models



@receiver(post_save, sender=Messages)
def create_message(sender, instance, created, **kwargs):
    if created:
        order = instance.order.id
        message_order = MessageOrder.objects.filter(id=order).first()
        if message_order is not None:
            message_order.total_message += 1
            message_order.save()


@receiver(post_delete, sender=Messages)
def delete_message(sender, instance, **kwargs):
    order = instance.order.id
    message_order = MessageOrder.objects.filter(id=order).first()
    if message_order is not None:
        message_order.total_message -= 1
        message_order.save()


@receiver(post_save, sender=models.Profile)
def created(sender, instance, created, **kwargs):
    if created:
        user = instance
        order_message = MessageOrder.objects.create(
            owner=user
        )
