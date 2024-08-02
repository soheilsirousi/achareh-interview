from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from customer.models import ExtendedUser


@receiver(post_save, sender=User)
def create_user_details(instance, created, *args, **kwargs):
    if created:
        userd = ExtendedUser.objects.create(user=instance)
