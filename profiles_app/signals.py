from django.db.models.signals import post_save
from django.dispatch import receiver
from auth_app.models import UserProfile
from profiles_app.models import Profile

"""
Signal from auth_app UserProfile , when creating a new User , creating a Profile
"""

@receiver(post_save, sender=UserProfile)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=UserProfile)
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()