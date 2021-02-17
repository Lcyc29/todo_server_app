from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework_api_key.models import APIKey
import todo_server_app.settings as settings
# from .models import UserAPIKey


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        old_key = APIKey.objects.get(name=instance.id)
    except APIKey.DoesNotExist:
        api_key, key = APIKey.objects.create_key(name=instance.id)
        f = open("%s/.apikey" % settings.BASE_DIR, "a")
        f.write('%s=%s\n' % (instance.username, key))
        f.close()
