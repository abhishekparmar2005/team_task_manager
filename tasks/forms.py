from django import forms
from django.contrib.auth.models import User
from .models import Task


class TaskForm(forms.ModelForm):
    """Used by admin to create/edit tasks"""

    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Task title'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Describe the task'}),
            'due_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'assigned_to': forms.Select(attrs={'class': 'form-input'}),
        }

    def __init__(self, project=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if project:
            # only show members of this project for assignment
            self.fields['assigned_to'].queryset = project.members.all()
        else:
            self.fields['assigned_to'].queryset = User.objects.none()


class TaskStatusForm(forms.ModelForm):
    """Used by members to update their task status"""

    class Meta:
        model = Task
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-input'}),
        }
