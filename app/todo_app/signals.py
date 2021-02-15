from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .models import UserAPIKey

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        api = UserAPIKey.objects.create(user_id=instance)
        api.api_key = '123' # this can be used as a randomly generated token, but I'll just use a simple string for the demo


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userapikey.save()
    
