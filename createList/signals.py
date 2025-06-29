from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

# Guarantees that a profile exists for every user (not 100% needed, but good safeguard)
#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
#    print("signal code:", created)
#    if created:
#        Profile.objects.create(user=instance)
