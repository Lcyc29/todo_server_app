from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ToDoApp(models.Model):
    STAT = (
        ('1', 'Todo'),
        ('2', 'In Progress'),
        ('3', 'Done'),
    )
    task_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=False, null=True)
    task_title = models.CharField(max_length=2000, blank=True, default="")
    task_description = models.TextField(blank=True, default="")
    task_state = models.CharField(
        max_length=2, choices=STAT, default="1", blank=True, null=True)
    task_due_date = models.DateField(
        auto_now=False, auto_now_add=False, blank=True, null=True)

    class Meta:
        ordering = ['task_id']

    def __str__(self):
        return str(self.task_id)


class UserAPIKey(models.Model):
    user_id = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=False, null=True)
    api_key = models.CharField(max_length=2000, blank=True, default="")

    class Meta:
        ordering = ['user_id']

    def __str__(self):
        return str(self.api_key)
