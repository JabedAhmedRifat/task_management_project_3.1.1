from django.db.models.signals import post_save
from django.dispatch import receiver

from user.models import UserProfile
from .models import *


# when task create task assignee notification created
@receiver(post_save, sender=Task)
def create_task_notification(sender, instance, created, **kwargs):
    if created:
        print(f"Task created: {instance.task_name}, assignee: {instance.assignee}")

        # Check if the task has an assignee
        if instance.assignee:
            print(f"Creating notification for assignee: {instance.assignee}")
            Notification.objects.create(
                user=instance.assignee,
                message=f"You have a new Task: {instance.task_name}",
            )





