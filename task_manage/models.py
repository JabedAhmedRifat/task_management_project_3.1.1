from django.db import models
from django.contrib.auth.models import User
from user.models import UserProfile
# from .models import 
# Create your models here.


class Notification(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    
    
class CheckListOption(models.Model):
    option_text = models.CharField(max_length=255, null=True, blank=True)




class Task(models.Model):
    task_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.URLField(null=True, blank=True) 
    task_submit = models.TextField(null=True, blank=True)
    assigner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='task_assigned')
    assignee = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='assigned_task')
    start_date= models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    due_date= models.DateTimeField(null=True)
    on_time_completion = models.BooleanField(default=False)
    PRIORITY_CHOICES = [
        ('low', 'low'),
        ('medium', 'medium'),
        ('high', 'high'),
    ]
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')
    STATUS_CHOICES= [
        ('todo','todo'),
        ('inprogress', 'inprogress'),
        ('pause','pause'),
        ('checklist', 'checklist'),
        ('qc_progress', 'qc_progress'),
        ('qc_complete', 'qc_complete'),
        ('done','done'),
    ]
    
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='todo')
    points= models.IntegerField(default=0)
    
    
    
    
    

    
class QCTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    check_text = models.ForeignKey(CheckListOption, on_delete=models.CASCADE)
    
    
 
class QCStatus(models.Model):
    qc = models.ForeignKey(QCTask, on_delete=models.CASCADE)
    is_checked = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)





class TaskHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    
    

class Notice(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    
    

class TaskActivity(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    status = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)