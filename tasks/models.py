from django.db import models
from django.contrib.auth.models import User
from projects.models import Project


class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def is_overdue(self):
        from django.utils import timezone
        if self.due_date and self.status != 'completed':
            return self.due_date < timezone.now().date()
        return False

    def next_status(self):
        transitions = {
            'pending': 'in_progress',
            'in_progress': 'completed',
        }
        return transitions.get(self.status)
