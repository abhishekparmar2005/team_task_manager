from django import forms
from django.contrib.auth.models import User
from .models import Project


class ProjectForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Team Members'
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'members']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Project name'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'What is this project about?'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show members (non-admins) as possible team members
        self.fields['members'].queryset = User.objects.select_related('profile').filter(
            profile__role='member'
        )
