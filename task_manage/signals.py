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



# # QC user create when register a new user
# @receiver(post_save, sender=UserProfile)
# def create_qc_user(sender, instance, created, **kwargs):
#     if created:
#         QCUser.objects.create(user=instance)





# @receiver(post_save, sender=Task)
# def create_qc_status(sender, instance, created, **kwargs):
#     if created:
#         print("Creating")
#         # Loop through each QCUser in the qc_check field and create a QCStatus for each
#         for qc_user in instance.qc_check.all():
#             QCStatus.objects.create(task=instance, user=qc_user, is_checked=False)
