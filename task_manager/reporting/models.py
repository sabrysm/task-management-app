from django.db import models
from task.models import Category


class TaskHistory(models.Model):
    title = models.CharField(max_length=255, default="Task")
    created_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Task History"
    
    
    