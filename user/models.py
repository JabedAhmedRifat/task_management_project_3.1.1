from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Target(models.Model):
    target = models.IntegerField(default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    TYPE=[
        ('superadmin','Super Admin'),
        ('admin','Admin'),
        ('member','Member'),
    ]
    type = models.CharField(max_length=20,choices=TYPE, default='member')
    score = models.IntegerField(default=0, null=True)
    image = models.URLField(null=True, blank=True) 
    category = models.CharField(max_length=100, null=True, blank=True)
    
    assigned_tasks_count = models.PositiveIntegerField(default=0)
    
    targetpoint = models.ForeignKey(Target, on_delete=models.CASCADE, null=True, blank=True)
