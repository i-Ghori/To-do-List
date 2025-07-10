from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tasks(models.Model):
    task = models.CharField(max_length=255)
    date = models.DateField(auto_now=True)
    is_done = models.BooleanField(null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")

    def __str__(self):
        return f"({self.user.username}) {self.task}"
    
    class Meta:
        verbose_name = "Tasks"
        verbose_name_plural = "Tasks"