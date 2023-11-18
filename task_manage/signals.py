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
                message=f"{instance.task_name}",
            )





@receiver(post_save, sender=Task)
def create_task_history(sender, instance, created, **kwargs):
    """
    Signal handler to create TaskHistory when a Task is created.
    """
    if created:
        TaskHistory.objects.create(task=instance, user=instance.assigner)