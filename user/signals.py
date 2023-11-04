from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, Target

@receiver(post_save, sender=UserProfile)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Target.objects.create(user=instance)

